$(document).ready(function() {
  $(".modalInput").overlay({mask: '#999', fixed: false}).bind("onBeforeClose", function(e) {
    $(".error").hide();
  });

  var schema;

  $.ajax({
    type: "GET",
    url: "/schema"
  }).done(function(schema) {
    // Print out the name of each table and their primary keys
    output = '';

    // For each table...
    $.each(schema, function(table, p_keys) {
      output += '<p>Table ' + table + ' has primary keys: ';

      // p_keys is the [(primary keys object), (headings objects)]
      $.each(p_keys, function(text, keys) {
        // text is either "primaryKey" or "column"

        if(text == "primary_keys") {
          $.each(keys, function(index, key) {
           output += key + ', ';
          });
        } else if (text == "columns") {
          output += " and has columns ";
          $.each(keys, function(index, key) {
            output += key + ', ';
          });
        }
      });
      output = output.substring(0, output.length - 2);
      output += '</p>';
    });

    $("#schema_table").html(output);
  });

  var unicode_chars = {
    "and": "\u2227",
    "or": "\u2228",
    "implies": "\u2192",
    "iff": "\u2194",
    "exists": "\u2203",
    "forall": "\u2200",
    "not": "\u00ac"
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

  $("#config_submit").click(function()  {
    user = $("#username_input").val();

    $.post(
      "/login", {
        username : user,
        password : $("#password_input").val(),
        host : $("#host_input").val(),
        port : $("#port_input").val(),
        dbname : $("#dbname_input").val() }
    ).done(function(response) {
      if (response.error === 'ok') {
        var n = noty({text: 'Configuration Accepted'})
        $(".close").trigger("click")
        n.fadeOut('slow')
      }
    });
  });

  /* When 'Convert to SQL' button is clicked fire off an AJAX request */
  $("#convert_button").click(function() {
    var input_string = $("textarea#logic").val();
    if(input_string !== "") {   
      $.ajax({
        type: "POST",
        data: {
          "logic" : input_string
        }
      }).done(function(response) {
        // Check the result of the translation and act appropriately
        if (response.status === 'ok') {
          var sql_result = response.sql;
          $("textarea#sql_result").text(sql_result);

          // Create an HTML table
          var table = '<table border="1" align="center"> <tr>';

          // Construct the header of the table from the query column names
          $.each(response.query_columns, function(i, column) {
            table += '<th>' + column + '</th>';
          });
          table += '</tr>';

          // Construct the body of the table from the query row data
          $.each(response.query_rows, function(i, row) {
            table += '<tr>';
            $.each(row, function(i, dataItem) {
              table += ('<td>' + dataItem + '</td>');
            });
            table += '</tr>'
          });

          // Add the resulting table to the page
          $("#results_table").html(table);
        } else {
          // Something went wrong, so print the error.
          if(response.sql !== '') {
            var sql_result = response.sql.concat("\n\n\nDatabase error message:\n", response.error);
          } else {
            var sql_result = response.error;
          }
          
          var sql_result_lines = sql_result.split("\n");  
          $("textarea#sql_result").text(sql_result);
          $("#results_table").html("");
        }
        
        var linecount = 0;
        var cols = 100;
        var sql_result_lines = sql_result.split("\n");
        $.each(sql_result_lines, function(l) {
          linecount += Math.ceil(l.length/cols);
        });
        $("textarea#sql_result").css("height", (linecount * 16 + 8).toString().concat("px"));
      });
    } else {
      $("textarea#sql_result").text("No input to convert");
    }
    return false;
  });

  // Convert characters to correct symbols
  $("textarea#logic").keypress(function(event) {
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

      // Go through all the possible formatters
      $.each(matching_formatters, function(index, regexResult) {
        // Check for a match
        portionMatch = portion.search(regexResult.regex);
        if (portionMatch != -1) {
          // Match found - replace text to action the formatter
          portion = portion.replace(regexResult.regex, regexResult.result);
          // Update the cursor as a result
          portionCursor = portionMatch + 1;
          // Break out of the loop - only one match allowed at the moment
          return false;
        }
      });

      // Put the modified portion back into the logic text
      logic = logic.substr(0, portionStart) + portion +
              logic.substr(portionEnd);
      cursor = portionStart + portionCursor;

      // Update the UI
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

  $("#not_button").click(function() {
    $("#logic").insertAtCursor(unicode_chars.not);
  });

  // Insert symbols at cursor position
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
        } else if ('selectionStart' in domElem ||
                   domElem.selectionStart == '0') {
          // For browsers like Firefox and Webkit based
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
