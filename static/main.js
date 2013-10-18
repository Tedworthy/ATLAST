/* When 'Convert to SQL' button is clicked fire off an AJAX request */
$(document).ready(function() {
  $('#convert_button').click(function () {
    var input_string = $("Textarea#logic").val();

    $.ajax({
      type: "POST",
      data: {
        'logic' : input_string
      }
    }).done(function(result) {
      /* Handle the result of the translation */
      $('#result').text(result);
    });
    return false;
  });
});
