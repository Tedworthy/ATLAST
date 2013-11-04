$(document).ready(function() {

  var keys = {
    "92": { "char": "\\", "formatters": ["and"] },
    "47": { "char": "/", "formatters": ["or"] },
    "62": { "char": ">", "formatters": ["implies"] },
    "69": { "char": "E", "formatters": ["there_exists"] },
    "65": { "char": "A", "formatters": ["forall"] }
  };

  var formatters = {
    "and": { "regex": /\/\\/g, "result": "\u22C0" },
    "or": { "regex": /\\\//g, "result": "\u22C1" },
    "implies": { "regex": /->/g, "result": "\u2192" },
    "there_exists": { "regex": /\\E/g, "result": "\u2203" },
    "forall": { "regex": /\\A/g, "result": "\u2200" }
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
  });
  
  $(function () {
    $('#and_button').on('click', function () {
        $('#logic').insertAtCaret(' \u22C0 ');
    });
  });

//http://stackoverflow.com/questions/1064089/inserting-a-text-where-cursor-is-using-javascript-jquery

 $.fn.extend({
  insertAtCaret: function(myValue){
  var obj;
  if( typeof this[0].name !='undefined' ) obj = this[0];
  else obj = this;
console.log();
  if ($.browser.msie) {
    obj.focus();
    sel = document.selection.createRange();
    sel.text = myValue;
    obj.focus();
    }
  else if ($.browser.mozilla || $.browser.webkit) {
    var startPos = obj.selectionStart;
    var endPos = obj.selectionEnd;
    var scrollTop = obj.scrollTop;
    obj.value = obj.value.substring(0, startPos)+myValue+obj.value.substring(endPos,obj.value.length);
    obj.focus();
    obj.selectionStart = startPos + myValue.length;
    obj.selectionEnd = startPos + myValue.length;
    obj.scrollTop = scrollTop;
  } else {
    obj.value += myValue;
    obj.focus();
   }
 }
})

// http://stackoverflow.com/questions/14798403/typeerror-browser-is-undefined
var matched, browser;

jQuery.uaMatch = function( ua ) {
    ua = ua.toLowerCase();

    var match = /(chrome)[ \/]([\w.]+)/.exec( ua ) ||
        /(webkit)[ \/]([\w.]+)/.exec( ua ) ||
        /(opera)(?:.*version|)[ \/]([\w.]+)/.exec( ua ) ||
        /(msie) ([\w.]+)/.exec( ua ) ||
        ua.indexOf("compatible") < 0 && /(mozilla)(?:.*? rv:([\w.]+)|)/.exec( ua ) ||
        [];

    return {
        browser: match[ 1 ] || "",
        version: match[ 2 ] || "0"
    };
};

matched = jQuery.uaMatch( navigator.userAgent );
browser = {};

if ( matched.browser ) {
    browser[ matched.browser ] = true;
    browser.version = matched.version;
}

// Chrome is Webkit, but Webkit is also Safari.
if ( browser.chrome ) {
    browser.webkit = true;
} else if ( browser.webkit ) {
    browser.safari = true;
}

jQuery.browser = browser;


});
