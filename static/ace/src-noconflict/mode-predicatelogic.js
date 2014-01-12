ace.define(
  'ace/mode/predicatelogic',

  ['require', 'exports', 'module', 'ace/lib/oop', 'ace/mode/text',
   'ace/tokenizer', 'ace/mode/predicatelogic_highlight_rules'],

  function(require, exports, module) {
    "use strict";
    var oop = require("../lib/oop");
    var TextMode = require("./text").Mode;
    var Tokenizer = require("../tokenizer").Tokenizer;
    var PredicateLogicHighlightRules =
      require("./predicatelogic_highlight_rules").PredicateLogicHighlightRules;
    var Mode = function() {
      this.HighlightRules = PredicateLogicHighlightRules;;
    };
    oop.inherits(Mode, TextMode);
    (function() {
      // Nothing to see here
    }).call(Mode.prototype);
    exports.Mode = Mode;
  }
);

ace.define(
  'ace/mode/predicatelogic_highlight_rules',

  ['require', 'exports', 'module', 'ace/lib/oop',
   'ace/mode/text_highlight_rules'],

  function(require, exports, module) {
    "use strict";

    var oop = require("../lib/oop");
    var TextHighlightRules =
      require("./text_highlight_rules").TextHighlightRules;

    var PredicateLogicHighlightRules = function() {
        this.$rules = {
            "start": [
                {
                    token: "whitespace",
                    regex: /[\t \n\r]+/
                }, {
                    token: "keyword",
                    regex: /(∃|∀)/,
                    next: "quantifier_identifier"
                }, {
                    token: "keyword",
                    regex: /(→|↔|∧|∨|¬)/
                }, {
                    token: "bracket",
                    regex: /(\(|\))/
                }, {
                    token: "atomicformula",
                    regex: "",
                    next: "atomicformula"
                }
            ],
            "quantifier_identifier": [
                {
                    token: "whitespace",
                    regex: /[\t \n\r]+/
                }, {
                    token: "variable",
                    regex: /[A-Za-z_][A-Za-z_\.0-9]*/,
                    next: "quantifier_identifier_list"
                }
            ],
            "quantifier_identifier_list": [
                {
                    token: "whitespace",
                    regex: /[\t \n\r]+/
                }, {
                    token: "comma",
                    regex: /,/,
                    next: "quantifier_identifier"
                }, {
                    token: "no_more_identifiers",
                    regex: "",
                    next: "quantifier_leftbracket"
                }
            ],
            "quantifier_leftbracket": [
                {
                    token: "whitespace",
                    regex: /[\t \n\r]+/
                }, {
                    token: "bracket",
                    regex: /\(/,
                    next: "start"
                }
            ],
            "atomicformula": [
                {
                    token: "whitespace",
                    regex: /[\t \n\r]+/
                }, {
                    token: "constant.numeric",
                    regex: /[0-9]+/,
                    next: "atomicformula_relop"
                }, {
                    token: "string",
                    regex: /('[^']*'|"[^"]*")/,
                    next: "atomicformula_relop"
                }, {
                    token: "constant.language.boolean",
                    regex: /(True|False)/,
                    next: "atomicformula_relop"
                }, {
                    token: "variable",
                    regex: /[A-Za-z_][A-Za-z_\.0-9]*/,
                    next: "atomicformula_identifier"
                }
            ],
            "atomicformula_identifier": [
                {
                    token: "whitespace",
                    regex: /[\t \n\r]+/
                }, {
                    token: "relop",
                    regex: /(=|≠|>|≥|<|≤)/,
                    next: "atomicformula_relop_term"
                }, {
                    token: "bracket",
                    regex: /\(/,
                    next: "atomicformula_predicate_term"
                }
            ],
            "atomicformula_relop": [
                {
                    token: "whitespace",
                    regex: /[\t \n\r]+/
                }, {
                    token: "relop",
                    regex: /(=|≠|>|≥|<|≤)/,
                    next: "atomicformula_relop_term"
                }
            ],
            "atomicformula_relop_term": [
                {
                    token: "whitespace",
                    regex: /[\t \n\r]+/
                }, {
                    token: "constant.numeric",
                    regex: /[0-9]+/,
                    next: "start"
                }, {
                    token: "string",
                    regex: /('[^']*'|"[^"]*")/,
                    next: "start"
                }, {
                    token: "constant.language.boolean",
                    regex: /(True|False)/,
                    next: "start"
                }, {
                    token: "variable",
                    regex: /[A-Za-z_][A-Za-z_\.0-9]*/,
                    next: "start"
                }
            ],
            "atomicformula_predicate_term": [
                {
                    token: "whitespace",
                    regex: /[\t \n\r]+/
                }, {
                    token: "constant.numeric",
                    regex: /[0-9]+/,
                    next: "atomicformula_predicate_term_list"
                }, {
                    token: "string",
                    regex: /('[^']*'|"[^"]*")/,
                    next: "atomicformula_predicate_term_list"
                }, {
                    token: "constant.language.boolean",
                    regex: /(True|False)/,
                    next: "atomicformula_predicate_term_list"
                }, {
                    token: "variable",
                    regex: /[A-Za-z_][A-Za-z_\.0-9]*/,
                    next: "atomicformula_predicate_term_list"
                }
            ],
            "atomicformula_predicate_term_list": [
                {
                    token: "comma",
                    regex: /,/,
                    next: "atomicformula_predicate_term"
                }, {
                    token: "no_more_terms",
                    regex: "",
                    next: "atomicformula_predicate_rightbracket"
                }
            ],
            "atomicformula_predicate_rightbracket": [
                {
                    token: "bracket",
                    regex: /\)/,
                    next: "start"
                }
            ]
        };
    };

    oop.inherits(PredicateLogicHighlightRules, TextHighlightRules);

    exports.PredicateLogicHighlightRules = PredicateLogicHighlightRules;
  }
);
