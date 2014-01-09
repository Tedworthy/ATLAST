$(document).ready(function() {

  // Extend strings to check for their presence in another array
  String.prototype.existsIn = function(array) {
    return array.indexOf(this.toString()) != -1;
  }

  var removeErrorLines = function() {
    var console = $("#errors_container").children("div:first-child");
    if (console.hasClass("errors")) {
      console.removeClass("errors");
      console.addClass("no_errors");
      console.children("i").removeClass("fa-exclamation-circle");
      console.children("i").addClass("fa-check-circle");
    }
    $("#errors_container").html(console);
  };

  var addErrorLine = function(message) {
    var console = $("#errors_container").children("div:first-child");
    if (console.hasClass("no_errors")) {
      console.removeClass("no_errors");
      console.addClass("errors");
      console.children("i").removeClass("fa-check-circle");
      console.children("i").addClass("fa-exclamation-circle");
    }
    var icon = $("<i>").addClass("fa fa-exclamation");
    var span = $("<span>").text(message);
    $("#errors_container").append($("<div>").append(icon).append(span));
  };

  var handleErrors = function(response) {
    // TODO
    switch (response.status) {
      case "db_error":

        break;
      case "parse_error":
        $.each(response.error, function(index, error) {
          switch (error.type) {
            case "ParserEOIException":
              addErrorLine("Logic input finished too soon. Did you perhaps " +
                           "forget an ending bracket or quote mark?");
              break;
            case "ParserTokenException":
              addErrorLine("Line " + error.lineNo + ", position " +
                           error.position + ": Unexpected '" + error.token +
                           "', perhaps check your logic syntax?");
              break;
          }
        });
        break;
      default:

        break;
    }
  };

  var windows = {
    "#query": "#query_container",
    "#help": "#help_container",
    "#settings": "#settings_container"
  };
  var current_window = "";

  $(window).on('hashchange', function() {
    if (document.location.hash in windows) {
      $("html, body").animate({ scrollTop: 0 }, "fast");
      if (current_window !== "")
        $(windows[current_window]).addClass("hidden");
      $(windows[document.location.hash]).removeClass("hidden");
      current_window = document.location.hash;
    } else {
      document.location.hash = "#query";
    }
  });

  $(window).trigger('hashchange');

  var logicEditor = ace.edit("logic");
  logicEditor.setTheme("ace/theme/solarized_dark");
  logicEditor.getSession().setMode("ace/mode/predicatelogic");

  var sqlEditor = ace.edit("sql");
  sqlEditor.setTheme("ace/theme/solarized_dark");
  sqlEditor.getSession().setMode("ace/mode/sql");
  sqlEditor.setReadOnly(true);
  sqlEditor.setOptions({
    maxLines: 10
  });

  var schema;
  $.ajax({
    type: "GET",
    url: "/schema"
  }).done(function(schema) {
    // Schema header
    var header = $("<div>").attr("id", "schema_header");
    var header_i = $("<i>").addClass("icon icon-db");
    // TODO change 'filmdb' to DB name from schema, when it's there...
    var header_span = $("<span>").html("filmdb");
    header.append(header_i).append(header_span);

    // Schema tables
    var tables = $("<div>").attr("id", "schema_tables");

    // For each table...
    $.each(schema, function(table_name, table) {
      var table_div = $("<div>").addClass("schema_table");
      var table_header = $("<div>");
      var table_header_i = $("<i>").addClass("fa fa-table");
      var table_header_span = $("<span>").text(table_name);
      table_header.append(table_header_i).append(table_header_span);
      table_div.append(table_header);

      var columns = [];

      $.each(table.columns, function(column_name, column) {
        var column_div = $("<div>");
        var column_span = $("<span>").text(column_name);
        var column_button = $("<button>");
        var column_button_i = $("<i>").addClass("fa fa-chevron-right");
        column_button.append(column_button_i);
        column_div.append(column_span).append(column_button);
        columns.push(column_div);
      });

      $.each(table.primary_keys, function(index, key) {
        $.each(columns, function(index, column) {
          if (column.children("span").text() === key) {
            column.addClass("key");
            var key_i = $("<i>").addClass("fa fa-key");
            column.prepend(key_i);
            return false;
          }
        });
      });

      $.each(columns, function(index, column) {
        table_div.append(column);
      });

      tables.append(table_div);
    });

    $("#schema_section").append(header).append(tables);

    // Schema buttons
    $("div.schema_table > div > button").on("click", function() {
      var regex = /(^|>) *([^ <>]+) *(<|$)/;
      var header = $(this).parent().parent().children("div:first-child");
      var row = $(this).parent();
      var table_name = header.html().match(regex)[2];
      var column_name = row.html().match(regex)[2];
      logicEditor.insert(table_name + "_" + column_name + "(, )");
      logicEditor.selection.moveCursorBy(0, -3);
      logicEditor.focus();
    });
  });

  var unicode_chars = {
    "and": "\u2227",
    "or": "\u2228",
    "implies": "\u2192",
    "iff": "\u2194",
    "exists": "\u2203",
    "forall": "\u2200",
    "not": "\u00ac",
    "not_equal": "\u2260"
  }

  var keys = {
    "92": { char: "\\", formatters: ["and", "or", "exists", "forall"] },
    "47": { char: "/", formatters: ["or", "and", "not_equal_slash"] },
    "60": { char: "<", formatters: ["iff", "implies"] },
    "45": { char: "-", formatters: ["iff", "implies"] },
    "62": { char: ">", formatters: ["iff", "implies"] },
    "69": { char: "E", formatters: ["exists"] },
    "65": { char: "A", formatters: ["forall"] },
    "33": { char: "!", formatters: ["not_equal_bang"] },
    "61": { char: "=", formatters: ["not_equal_slash", "not_equal_bang"] },
    "126": { char: "~", formatters: ["not"] }
  };

  var formatters = {
    "and": { regex: /\/\\/, result: unicode_chars.and },
    "or": { regex: /\\\//, result: unicode_chars.or },
    "implies": { regex: /->/, result: unicode_chars.implies },
    "iff": { regex: /<->/, result: unicode_chars.iff },
    "exists": { regex: /\\E/, result: unicode_chars.exists },
    "forall": { regex: /\\A/, result: unicode_chars.forall },
    "not": { regex: /~/, result: unicode_chars.not },
    "not_equal_slash": { regex: /\/=/, result: unicode_chars.not_equal },
    "not_equal_bang": { regex: /!=/, result: unicode_chars.not_equal }
  };

  $("#config_submit").click(function()  {
    $.post(
      "/login",
      {
        username: $("#username_input").val(),
        password: $("#password_input").val(),
        host: $("#host_input").val(),
        port: $("#port_input").val(),
        dbname: $("#dbname_input").val()
      }
    ).done(function(response) {
      if (response.error === 'ok') {
        var n = noty({text: 'Configuration Accepted'})
        $(".close").trigger("click")
        n.fadeOut('slow')
      }
    });
  });

  /* When 'Convert to SQL' button is clicked fire off an AJAX request */
  $("#logic-form").submit(function(e) {
    e.preventDefault();
    var input_string = logicEditor.getValue();
    if (input_string !== "") {
      $.post(
        "/",
        {
          logic: input_string
        }
      ).done(function(response) {
        // Check the result of the translation and act appropriately
        if (response.status === 'ok') {
          // Create an HTML table
          var table = '<table> <tr>';

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
            table += '</tr>';
          });
          table += '</table>';

          // Add the resulting table to the page
          removeErrorLines();
          $("#results_table").html(table);
          sqlEditor.setValue(response.sql);
        } else {
          // Something went wrong, so print the error.
          removeErrorLines();
          handleErrors(response);
          $("#results_table").html("");
          sqlEditor.setValue("-- Something went wrong, see the console above");
        }
      });
    } else {
      sqlEditor.setValue("-- SQL query will appear here");
    }
  });

  // Convert characters to correct symbols
  $(logicEditor.container).on('keypress', function(e) {
    // TODO REMOVE THIS LATER, IT'S DEBUGGING CODE
    console.log("Key down:" + e.keyCode);

    // Firefox / Chrome compatibility
    var k = (typeof e.which === "number") ? e.which : e.keyCode;

    var key = keys[k.toString()];
    if (key !== undefined) {
      // Stop the keypress from happening normally
      e.preventDefault();

      // Get the relevant formatters for the pressed key
      var matching_formatters = key.formatters.map(function(name) {
        return formatters[name];
      });

      if (!(logicEditor.selection.isEmpty()))
        logicEditor.session.remove(logicEditor.selection.getRange());

      // Get current state
      var ace_cursor = logicEditor.selection.getCursor();
      var logic = logicEditor.getValue();

      var cursor = rowColumnToCursor(ace_cursor, logic);

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

      ace_cursor = cursorToRowColumn(cursor, logic);

      // Update the UI
      logicEditor.setValue(logic);
      logicEditor.selection.clearSelection();
      logicEditor.selection.moveCursorToPosition(ace_cursor);
    }
  });

  // Buttons that insert symbols
  $("#and_button").click(function() {
    logicEditor.insert(unicode_chars.and);
    logicEditor.focus();
  });

  $("#or_button").click(function() {
    logicEditor.insert(unicode_chars.or);
    logicEditor.focus();
  });

  $("#implies_button").click(function() {
    logicEditor.insert(unicode_chars.implies);
    logicEditor.focus();
  });

  $("#iff_button").click(function() {
    logicEditor.insert(unicode_chars.iff);
    logicEditor.focus();
  });

  $("#exists_button").click(function() {
    logicEditor.insert(unicode_chars.exists);
    logicEditor.focus();
  });

  $("#forall_button").click(function() {
    logicEditor.insert(unicode_chars.forall);
    logicEditor.focus();
  });

  $("#not_button").click(function() {
    logicEditor.insert(unicode_chars.not);
    logicEditor.focus();
  });

  var rowColumnToCursor = function(row_column, text) {
    var cursor = 0;
    var row = row_column.row;
    var match;
    while (row > 0) {
      match = text.substr(cursor).search("\n");
      if (match == -1)
        break;
      cursor += match + 1;
      row--;
    }
    cursor += row_column.column;
    return cursor;
  };

  var cursorToRowColumn = function(cursor, text) {
    var considered_text = text.substr(0, cursor);
    var temp_cursor = 0;
    var row = 0;
    while (considered_text.substr(temp_cursor).search("\n") != -1) {
      temp_cursor += considered_text.substr(temp_cursor).search("\n");
      row++;
    }
    var lastNewline = text.lastIndexOf("\n");
    lastNewline = (lastNewline = -1) ? 0 : lastNewline;
    var column = cursor - lastNewline;
    return { "row": row, "column": column };
  };

  // TODO REMOVE LEGACY CODE - Insert symbols at cursor position
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
