import ply.lex as lex 

tokens = (
  "FORALL",
  "THEREEXISTS",
  "TRUE",
  "FALSE",
  "OR",
  "AND",
  "IMPLIES",
  "IFF",
  "GT",
  "LT",
  "GTE",
  "LTE",
  "EQ",
  "LBRACKET",
  "RBRACKET",
  "COMMA",
  "NOT",
  "VARIABLE",
  "IDENTIFIER",
  "CONSTANT",
  "STRINGLIT"
)

t_FORALL = u"\u2200"
t_THEREEXISTS = u"\u2203"
t_TRUE = "True"
t_FALSE = "False"
t_OR = u"\u2228"
t_AND = u"\u2227"
t_IMPLIES = u"\u2192"
t_IFF = u"\u2194"
t_GT = ">"
t_LT = "<"
t_GTE = u"\u2265"
t_LTE = u"\u2264"
t_EQ = "="
t_LBRACKET = "\("
t_RBRACKET = "\)"
t_COMMA = ","
t_NOT = u"\u00AC"

digit = r'([0-9])'
nondigit = r'([_A-Za-z])'

t_IDENTIFIER = r'(' + digit + r'|' + nondigit + ')+'
t_CONSTANT = r'[A-Z]+'
def t_STRINGLIT(t):
  r'\'(.*)\''
  t.value = t.value[1:-1]
  return t

literals = '+-*/'
t_ignore = ' '

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

def t_error(t):
  print "Illegal character '%s'" % t.value[0]
  t.lexer.skip(1)

lex.lex()
