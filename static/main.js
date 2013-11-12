$(document).ready(function() {

  var schema;

  $.ajax({
    type: "GET",
    url: "/schema"    
  }).done(function(result) {
    schema = $.parseJSON(result);     
  });

  var unicode_chars = {
    "and": "\u22C0",
    "or": "\u22C1",
    "implies": "\u2192",
    "iff": "\u2194",
    "exists": "\u2203",
    "forall": "\u2200"
  }

  var keys = {
    "92": { "char": "\\", "formatters": ["and", "or", "exists", "forall"] },
    "47": { "char": "/", "formatters": ["or", "and"] },
    "60": { "char": "<", "formatters": ["iff", "implies"] },
    "45": { "char": "-", "formatters": ["iff", "implies"] },
    "62": { "char": ">", "formatters": ["iff", "implies"] },
    "69": { "char": "E", "formatters": ["exists"] },
    "65": { "char": "A", "formatters": ["forall"] }
  };

  var formatters = {
    "and": { "regex": /\/\\/, "result": unicode_chars.and },
    "or": { "regex": /\\\//, "result": unicode_chars.or },
    "implies": { "regex": /->/, "result": unicode_chars.implies },
    "iff": { "regex": /<->/, "result": unicode_chars.iff },
    "exists": { "regex": /\\E/, "result": unicode_chars.exists },
    "forall": { "regex": /\\A/, "result": unicode_chars.forall }
  };

  // Extend String objects with custom regex match/search function
  String.prototype.matchPortion = function(regex) {
    var search = this.search(regex);
    if (search == -1)
      return null;
    var matches = this.match(regex);
    return {
        "start": search,
        "end": search + matches[0].length
      };
  }

  /* When 'Convert to SQL' button is clicked fire off an AJAX request */
  $("#convert_button").click(function() {
    var input_string = $("textarea#logic").val();
    $.ajax({
      type: "POST",
      data: {
        "logic" : input_string
      }
    }).done(function(result) {
      // Handle the result of the translation
      var response = $.parseJSON(result);

      // Print out SQL query produced and the returned JSON object
      if(response.error === 'ok') {
        $("textarea#sql_result").text(response.sql);
      } else {
        $("textarea#sql_result").text(response.error);
      }

      $("textarea#query_result").text(JSON.stringify(response) + "\n");

      var table = "";
      // If the query result has no rows
      if(response.query.length == 0) {
        table = "Query returned no results";
      } else {
        // Print column headings for result data
        table = '<table border="1" align="center"><tr>';
        var first_row = response.query[0];
        $.each(first_row, function(k, v) {
          table += '<th>' + k + '</th>';
        });
        table += '</tr>';

        // loop over each object in the array to create table rows
        $.each(response.query, function() {
          table += '<tr>';
          $.each(this, function(k, v) {
            table += ('<td>' + v + '</td>');
          });
          table += '</tr>';
        });
      }

      // Add the resulting table to the page
      $("#results_table").html(table);
    });
    return false;
  });

  // Convert characters to correct symbols
  $("textarea#logic").keypress(function(event) {
    // TODO Debug - remove when finished with this
    console.log("Key down:" + event.keyCode);

    // Firefox / Chrome compatibility
    var k = (typeof event.which === "number") ? event.which : event.keyCode;

    var key = keys[k.toString()];
    if (key !== undefined) {
      // Stop the keypress from happening normally
      event.preventDefault();

      // Get the relevant formatters for the pressed key
      var matching_formatters = key.formatters.map(function(name) {
        return formatters[name];
      });

      // Get current state
      var cursor = $(this).getCursorPosition();
      var logic = $(this).val();

      // Augment the existing logic as if the pressed key had been inserted
      logic = logic.substr(0, cursor) + key.char + logic.substr(cursor);
      cursor += 1;

      // Take (at most) a 10 character portion of the logic text around cursor
      var portionStart = Math.max(0, cursor - 5);
      var portionCursor = cursor - portionStart;
      var portion = logic.substr(portionStart, 10);
      var portionEnd = portionStart + portion.length;

      // Go through all possible formatters
      $.each(matching_formatters, function(index, regex_result) {
        // Check for a match
        portion_match = portion.matchPortion(regex_result.regex);
        if (portion_match != null) {
          // Match found - replace text to action the formatter
          portion = portion.replace(regex_result.regex, regex_result.result);
          // Update the cursor as a result
          portionCursor = portion_match.start + 1;
          // Break out of the loop - only one match allowed at the moment
          return false;
        }
      });

      logic = logic.substr(0, portionStart) + portion
              + logic.substr(portionEnd);
      cursor = portionStart + portionCursor;

      $(this).val(logic);
      $(this).setCursorPosition(cursor);
    }
  });

  // Buttons insert correct symbols
  $("#and_button").click(function() {
    $("#logic").insertAtCursor(unicode_chars.and);
  });

  $("#or_button").click(function() {
    $("#logic").insertAtCursor(unicode_chars.or);
  });

  $("#implies_button").click(function() {
    $("#logic").insertAtCursor(unicode_chars.implies);
  });

  $("#iff_button").click(function() {
    $("#logic").insertAtCursor(unicode_chars.iff);
  });

  $("#exists_button").click(function() {
    $("#logic").insertAtCursor(unicode_chars.exists);
  });

  $("#forall_button").click(function() {
    $("#logic").insertAtCursor(unicode_chars.forall);
  });

  // Add textarea cursor manipulation functions to jQuery
  // All three functions based on code from StackOverflow
  $.fn.extend({
    insertAtCursor:
      function(text) {
        var domElem = $(this).get(0);
        if ('selection' in document) {
          // For browsers like Internet Explorer
          domElem.focus();
          var sel = document.selection.createRange();
          sel.text = text;
          domElem.focus();
        } else if ('selectionStart' in domElem || domElem.selectionStart == '0') {
          // For browsers like Firefox and WebKit-based
          var startPos = domElem.selectionStart;
          var endPos = domElem.selectionEnd;
          var scrollTop = domElem.scrollTop;
          domElem.value = domElem.value.substring(0, startPos) + text +
            domElem.value.substring(endPos, domElem.value.length);
          domElem.focus();
          domElem.selectionStart = startPos + text.length;
          domElem.selectionEnd = startPos + text.length;
          domElem.scrollTop = scrollTop;
        } else {
          domElem.value += text;
          domElem.focus();
        }
      },
    getCursorPosition:
      function() {
        var domElem = $(this).get(0);
        var pos = 0;
        if ('selectionStart' in domElem) {
          pos = domElem.selectionStart;
        } else if ('selection' in document) {
          domElem.focus();
          var sel = document.selection.createRange();
          var selLength = document.selection.createRange().text.length;
          sel.moveStart('character', -domElem.value.length);
          pos = sel.text.length - selLength;
        }
        return pos;
      },
    setCursorPosition:
      function(pos) {
        var domElem = $(this).get(0);
        if ('setSelectionRange' in domElem) {
          domElem.setSelectionRange(pos, pos);
        } else if ('createTextRange' in domElem) {
          var range = domElem.createTextRange();
          range.collapse(true);
          range.moveEnd('character', pos);
          range.moveStart('character', pos);
          range.select();
        }
      }
  });

});
