$(document).ready(function() {

  var keys = {
    "92": { "char": "\\", "formatters": ["and"] },
    "62": { "char": ">", "formatters": ["implies"] }
  }

  var formatters = {
    "and": { "regex": /\/\\/g, "result": "\u2227" },
    "implies": { "regex": /->/g, "result": "\u2192" }
  };

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
      $("textarea#sql_result").text(response.sql);
      $("textarea#query_result").text(response.query);
    });
    return false;
  });

  $("textarea#logic").keypress(function(event) {
    console.log("Key down:" + event.keyCode);
    var key = keys[event.keyCode.toString()];
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
    //var logic = $(this).val();
    //if (logic.slice(-1) == "^") {
    //  $("textarea#sql_result").text("^ FOUND");
    //}
  });

});
