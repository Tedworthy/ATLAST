$(document).ready(function() {

  /* When 'Convert to SQL' button is clicked fire off an AJAX request */
  $('#convert_button').click(function () {
    var input_string = $("textarea#logic").val();
    $.ajax({
      type: "POST",
      data: {
        'logic' : input_string
      }
    }).done(function(result) {
      /* Handle the result of the translation */
      $('textarea#sql_result').text(result);
    });
    return false;
  });

});
