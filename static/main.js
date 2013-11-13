$(document).ready(function() {
  $(".modalInput").overlay({mask: '#999', fixed: false}).bind("onBeforeClose", function(e) {
    $(".error").hide();
  });

  var unicode_chars = {
    "and": "\u22C0",
    "or": "\u22C1",
    "implies": "\u2192",
    "there_exists": "\u2203",
    "forall": "\u2200"
  }

  var keys = {
    "92": { "char": "\\", "formatters": ["and"] },
    "47": { "char": "/", "formatters": ["or"] },
    "62": { "char": ">", "formatters": ["implies"] },
    "69": { "char": "E", "formatters": ["there_exists"] },
    "65": { "char": "A", "formatters": ["forall"] }
  };

  var formatters = {
    "and": { "regex": /\/\\/g, "result": unicode_chars.and },
    "or": { "regex": /\\\//g, "result": unicode_chars.or },
    "implies": { "regex": /->/g, "result": unicode_chars.implies },
    "there_exists": { "regex": /\\E/g, "result": unicode_chars.there_exists },
    "forall": { "regex": /\\A/g, "result": unicode_chars.forall }
  };
  $("#config_submit").click(function()  {
    user = $("#user_input").val();

    $.post(
      "/login", "i like cheese"
      
        
    /*    user : user,
        password : $("#password_input").val(),
        host : $("#host_input").val(),
        port : $("#port_input").val(),
        dbname : $("#dbname_input").val() */
      
    ).done(function(result) {
      var response = $.parseJSON(result);
      if (response.error === 'ok') {
        $("#conmsg").fadeIn("slow");
        $("#conmsg a.close-notify").click(function() {
          $("#conmsg").fadeOut("slow");
          return false;
        });
      }
    });
  });
  /* When 'Convert to SQL' button is clicked fire off an AJAX request */
  $("#convert_button").click(function() {
    var input_string = $("textarea#logic").val();
    $.ajax({
      type: "POST",

      data: {
        "logic" : input_string
      }
    }).done(function(result) {
      /* Handle the result of the translation */
      var response = $.parseJSON(result);

      // Print out SQL query produced and the returned JSON object
      if(response.error === 'ok') {
        $("textarea#sql_result").text(response.sql);
      } else {
        $("textarea#sql_result").text("Failed to convert query into SQL");
      }
      
      $("textarea#query_result").text(JSON.stringify(response.query) + "\n");
      
      // Print rows from result of running query on database
      var table='<table border="1" align="center"> <tr>';
      var first_row = response.query[0];
      $.each(first_row, function(k, v) {
        table += '<th>' + k + '</th>';
      });
      table += '</tr>';
      
      // loop over each object in the array to create rows
      $.each(response.query, function() {
      table += '<tr>'
        $.each(this, function(k, v) {
          table += ('<td>' + v + '</td>');
        });
        
        table += '</tr>'
      });
      
      // Add the resulting table to the page
      $("#results_table").html(table);	
      
    });
    return false;
  });

  // Convert characters to correct symbols
  $("textarea#logic").keypress(function(event) {
    console.log("Key down:" + event.keyCode);
    
    // Firefox / Chrome compatibility
    var k = (typeof event.which === "number") ? event.which : event.keyCode;
    
    var key = keys[k.toString()];
    if (key !== undefined) {
      event.preventDefault();
      var matching_formatters = key.formatters.map(function(name) {
        return formatters[name];
      });
      var logic = $(this).val() + key.char;
      $.each(matching_formatters, function(index, regex_result) {
        logic = logic.replace(regex_result.regex, regex_result.result);
      });
      $(this).val(logic);
    }
  });

  // Buttons insert correct symbols
  $("#and_button").click(function() {
    $("#logic").insertAtCaret(unicode_chars.and);
  });

  $("#or_button").click(function() {
    $("#logic").insertAtCaret(unicode_chars.or);
  });
  
  $("#implies_button").click(function() {
    $("#logic").insertAtCaret(unicode_chars.implies);
  });
  
  $("#there_exists_button").click(function() {
    $("#logic").insertAtCaret(unicode_chars.there_exists);
  });
  
  $("#forall_button").click(function() {
    $("#logic").insertAtCaret(unicode_chars.forall);
  });
  
  
  

  // Insert symbols at cursor position
  $.fn.extend({
    insertAtCaret: function(text) {
      return this.each(function(i) {
        if (document.selection) {
          // For browsers like Internet Explorer
          this.focus();
          var sel = document.selection.createRange();
          sel.text = text;
          this.focus();
        } else if (this.selectionStart || this.selectionStart == '0') {
          // For browsers like Firefox and Webkit based
          var startPos = this.selectionStart;
          var endPos = this.selectionEnd;
          var scrollTop = this.scrollTop;
          this.value = this.value.substring(0, startPos) + text +
            this.value.substring(endPos, this.value.length);
          this.focus();
          this.selectionStart = startPos + text.length;
          this.selectionEnd = startPos + text.length;
          this.scrollTop = scrollTop;
        } else {
          this.value += text;
          this.focus();
        }
      });
    }
  });

});
