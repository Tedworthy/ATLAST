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
        addErrorLine("Database error: " + response.error);
        break;
      case "parse_error":
        $.each(response.error, function(index, error) {
          switch (error.type) {
            case "ParserEOIException":
              addErrorLine("Logic input finished too soon, did you perhaps " +
                           "forget an ending bracket or quote mark?");
              break;
            case "ParserTokenException":
              addErrorLine("Line " + error.line + ", position " +
                           error.position + ": unexpected '" + error.token +
                           "', perhaps check your logic syntax?");
              break;
            case "LexerException":
              addErrorLine("Line " + error.line + ", position " +
                           error.position + ": invalid character '" +
                           error.character + "' encountered, perhaps remove " +
                           "it or check your logic syntax?");
              break;
          }
        });
        break;
      case "semantic_error":
        $.each(response.error, function (index, error) {
          switch (error.type) {
            case "SemanticSchemaRelationException":
              addErrorLine("Line " + error.line + ", position " +
                           error.position + ": relation '" + error.relation +
                           "' does not exist in the database, perhaps check " +
                           "the schema above?");
              break;
            case "SemanticSchemaAttributeException":
              addErrorLine("Line " + error.line + ", position " +
                           error.position + ": attribute '" + error.attribute +
                           "' does not exist in the relation '" +
                           error.relation + "', perhaps check the schema " +
                           "above?");
              break;
          }
        });
        break;
      default:
        addErrorLine("Something very strange happened, and we're not sure " +
                     "what. Please let us know your logic!");
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
    $("#settings_result_section").addClass("hidden");
  });

  $(window).trigger('hashchange');

  var logicEditor = ace.edit("logic");
  logicEditor.setTheme("ace/theme/solarized_dark");
  logicEditor.getSession().setMode("ace/mode/predicatelogic");
  logicEditor.setOptions({
    minLines: 6,
    maxLines: 15
  });

  var sqlEditor = ace.edit("sql");
  sqlEditor.setTheme("ace/theme/solarized_dark");
  sqlEditor.getSession().setMode("ace/mode/sql");
  sqlEditor.setReadOnly(true);
  sqlEditor.setOptions({
    minLines: 3,
    maxLines: 10
  });

  var refresh_schema = function() {
    $.ajax({
      type: "GET",
      url: "/schema"
    }).done(function(schema) {
      $("#schema_section").html("");

      // Schema header
      var header = $("<div>").attr("id", "schema_header");
      var header_i = $("<i>").addClass("icon icon-db");
      var header_span = $("<span>").text(schema.dbname);
      header.append(header_i).append(header_span);

      // Schema tables
      var tables = $("<div>").attr("id", "schema_tables");

      // For each table...
      $.each(schema.tables, function(table_name, table) {
        var table_div = $("<div>").addClass("schema_table");
        var table_header = $("<div>");
        var table_header_i = $("<i>").addClass("fa fa-table");
        var table_header_span = $("<span>").addClass("table").text(table_name);
        table_header.append(table_header_i).append(table_header_span);
        table_div.append(table_header);

        var columns = [table.columns.length];

        // For each column...
        $.each(table.columns, function(column_name, column) {
          var column_div = $("<div>");
          var column_span_name = $("<span>").text(column_name);
          column_span_name.addClass("column");
          var type = column.type;
          switch (column.type) {
            case "double precision":
              type = "double";
            case "character":
            case "character varying":
              type = "string";
              break;
            default:
              type = column.type;
              break;
          }
          type = " : " + type;
          var column_span_type = $("<span>").text(type);
          var column_button = $("<button>");
          var column_button_i = $("<i>").addClass("fa fa-chevron-right");
          column_button.append(column_button_i);
          column_div.append(column_span_name).append(column_span_type);
          column_div.append(column_button);
          columns[column.ordinal - 1] = column_div;
        });

        // Mark the key fields with icons
        $.each(table.primary_keys, function(index, key) {
          $.each(columns, function(index, column) {
            if (column.children("span.column").text() === key) {
              column.addClass("key");
              var key_i = $("<i>").addClass("fa fa-key");
              column.prepend(key_i);
              return false;
            }
          });
        });

        // Build up the table
        $.each(columns, function(index, column) {
          table_div.append(column);
        });

        tables.append(table_div);
      });

      $("#schema_section").append(header).append(tables);

      // Schema buttons
      $("div.schema_table > div > button").on("click", function() {
        var header = $(this).parent().parent().children("div:first-child");
        var row = $(this).parent();
        var table_name = header.children("span.table").text();
        var column_name = row.children("span.column").text();
        logicEditor.insert(table_name + "." + column_name + "(, )");
        logicEditor.selection.moveCursorBy(0, -3);
        logicEditor.focus();
      });
    });
  };

  // Call refresh_schema when the page loads
  refresh_schema();

  var unicode_chars = {
    and: "\u2227",
    or: "\u2228",
    implies: "\u2192",
    iff: "\u2194",
    exists: "\u2203",
    forall: "\u2200",
    not: "\u00ac",
    not_equal: "\u2260",
    less_equal: "\u2264",
    greater_equal: "\u2265"
  }

  var keys = {
    "92": { char: "\\", formatters: ["and", "or", "exists", "forall"] },
    "47": { char: "/", formatters: ["or", "and", "not_equal_slash"] },
    "60": { char: "<", formatters: ["iff", "implies", "less_equal"] },
    "45": { char: "-", formatters: ["iff", "implies"] },
    "62": { char: ">", formatters: ["iff", "implies", "greater_equal"] },
    "69": { char: "E", formatters: ["exists"] },
    "65": { char: "A", formatters: ["forall"] },
    "33": { char: "!", formatters: ["not_equal_bang"] },
    "61": { char: "=", formatters: ["not_equal_slash", "not_equal_bang",
                                    "greater_equal", "less_equal"] },
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
    "not_equal_bang": { regex: /!=/, result: unicode_chars.not_equal },
    "less_equal": { regex: /<=/, result: unicode_chars.less_equal },
    "greater_equal": { regex: />=/, result: unicode_chars.greater_equal }
  };

  $("#settings_form").submit(function(e) {
    e.preventDefault();
    $.post(
      "/settings",
      {
        username: $("#settings_username").val(),
        password: $("#settings_password").val(),
        host: $("#settings_server").val(),
        port: $("#settings_port").val(),
        dbname: $("#settings_dbname").val()
      }
    ).done(function(response) {
      var result_line = $("#settings_result_line");
      var class_to_remove, class_to_add;
      var i_class_to_remove, i_class_to_add;
      if (response.status === "ok") {
        class_to_add = "no_errors";
        class_to_remove = "errors";
        i_class_to_add = "fa-check-circle";
        i_class_to_remove = "fa-exclamation-circle";
        result_line.children("span").text("Connected to database successfully");
        refresh_schema();
        logicEditor.setValue("");
      } else {
        class_to_add = "errors";
        class_to_remove = "no_errors";
        i_class_to_add = "fa-exclamation-circle";
        i_class_to_remove = "fa-check-circle";
        result_line.children("span").text("Couldn't connect: " +
                                          response.error);
      }
      result_line.removeClass(class_to_remove);
      result_line.addClass(class_to_add);
      result_line.children("i").removeClass(i_class_to_remove);
      result_line.children("i").addClass(i_class_to_add);
      result_line.parent().parent().removeClass("hidden");
    });
  });

  /* When 'Convert to SQL' button is clicked fire off an AJAX request */
  $("#logic_form").submit(function(e) {
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
          sqlEditor.setValue(response.sql + "\n");
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

  $("#not_button").click(function() {
    logicEditor.insert(unicode_chars.not);
    logicEditor.focus();
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

  $("#equal_button").click(function() {
    logicEditor.insert("=");
    logicEditor.focus();
  });

  $("#not_equal_button").click(function() {
    logicEditor.insert(unicode_chars.not_equal);
    logicEditor.focus();
  });

  $("#less_button").click(function() {
    logicEditor.insert("<");
    logicEditor.focus();
  });

  $("#less_equal_button").click(function() {
    logicEditor.insert(unicode_chars.less_equal);
    logicEditor.focus();
  });

  $("#greater_button").click(function() {
    logicEditor.insert(">");
    logicEditor.focus();
  });

  $("#greater_equal_button").click(function() {
    logicEditor.insert(unicode_chars.greater_equal);
    logicEditor.focus();
  });

  $("#demo1").click(function() {
    logicEditor.setValue(unicode_chars.exists +
      "f,c,a(\n" +
      "    films.title(f, 'The Bourne Identity') " +
      unicode_chars.and + "\n" +
      "    casting.fid(c, f) " +
      unicode_chars.and + "\n" +
      "    casting.aid(c, a) " +
      unicode_chars.and + "\n" +
      "    actors.name(a, n) " +
      "\n)");
    logicEditor.focus();
  });

  $("#demo2").click(function() {
    logicEditor.setValue(unicode_chars.exists +
      "f,c,a,newc,newf(\n" +
      "    films.title(f, 'The Bourne Identity') " +
      unicode_chars.and + "\n" +
      "    casting.fid(c, f) " +
      unicode_chars.and + "\n" +
      "    casting.aid(c, a) " +
      unicode_chars.and + "\n" +
      "    actors.name(a, n) " +
      unicode_chars.and + "\n" +
      "    casting.aid(newc, a) " +
      unicode_chars.and + "\n" +
      "    casting.fid(newc, newf) " +
      unicode_chars.and + "\n" +
      "    films.title(newf, title)" +
      "\n)"
      );
    logicEditor.focus();
  });

  $("#demo3").click(function() {
    logicEditor.setValue(unicode_chars.exists + "cid,wid(\n" +
      "    character.charname(cid, name) " + unicode_chars.and + "\n" +
      "    character.description(cid, desc) " + unicode_chars.and + "\n" +
      "    characterr.speechcount(cid, sc) " + unicode_chars.and + "\n" +
      "    sc > 50 " + unicode_chars.and + "\n" +
      "    work.title(wid, play) " + unicode_chars.and + "\n" +
      "    character_work(cid, wid) " + unicode_chars.and + "\n" +
      "    (play = 'Othello' ∨ play = 'Macbeth')" + "\n" +
      ")");
    logicEditor.focus();
  });

  $("#demo4").click(function() {
    logicEditor.setValue(unicode_chars.exists + "x(\n" +
      "    films.director(x, dir) " + unicode_chars.and + "\n" +
      "    " + unicode_chars.forall + "y(\n" +
      "        films.director(y, dir) " + unicode_chars.implies + "\n" +
      "        (films.length(y, len) " + unicode_chars.and + " len > '2:00:00')\n" +
      "    )\n" +
      ")");
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
      temp_cursor += considered_text.substr(temp_cursor).search("\n") + 1;
      row++;
    }
    var column = cursor;
    if (row > 0)
      column -= considered_text.lastIndexOf("\n") + 1;
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
