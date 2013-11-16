import ply.lex as lex

class TokenEnum(object):
  FORALL = "FORALL"
  THEREEXISTS = "THEREEXISTS"
  TRUE = "TRUE"
  FALSE = "FALSE"
  OR = "OR"
  AND = "AND"
  IMPLIES = "IMPLIES"
  IFF = "IFF"
  GT = "GT"
  LT = "LT"
  GTE = "GTE"
  LTE = "LTE"
  EQ = "EQ"
  NEQ = "NEQ"
  LBRACKET = "LBRACKET"
  RBRACKET = "RBRACKET"
  COMMA = "COMMA"
  NOT = "NOT"
  VARIABLE = "VARIABLE"
  IDENTIFIER = "IDENTIFIER"
  CONSTANT = "CONSTANT"
  STRINGLIT = "STRINGLIT"

tokens = (
  TokenEnum.FORALL,
  TokenEnum.THEREEXISTS,
  TokenEnum.TRUE,
  TokenEnum.FALSE,
  TokenEnum.OR,
  TokenEnum.AND,
  TokenEnum.IMPLIES,
  TokenEnum.IFF,
  TokenEnum.GT,
  TokenEnum.LT,
  TokenEnum.GTE,
  TokenEnum.LTE,
  TokenEnum.EQ,
  TokenEnum.NEQ,
  TokenEnum.LBRACKET,
  TokenEnum.RBRACKET,
  TokenEnum.COMMA,
  TokenEnum.NOT,
  TokenEnum.VARIABLE,
  TokenEnum.IDENTIFIER,
  TokenEnum.CONSTANT,
  TokenEnum.STRINGLIT
)

t_FORALL = u"\u2200"
t_THEREEXISTS = u"\u2203"
t_TRUE = 'True'
t_FALSE = 'False'
t_OR = u"\u2228"
t_AND = u"\u2227"
t_IMPLIES = u"\u2192"
t_IFF = u"\u2194"
t_GT = ">"
t_LT = "<"
t_GTE = u">="
t_LTE = u"<="
t_EQ = "="
t_NEQ = u"\u2260"
t_LBRACKET = "\("
t_RBRACKET = "\)"
t_COMMA = ","
t_NOT = u"\u00AC"

digit = r'([0-9])'
nondigit = r'([_A-Za-z])'

# Literals are passed straight through as their own token
literals = '+-*/'
# Spaces are taken out completely
t_ignore = ' '

t_CONSTANT = r'[A-Z]+'

reserved = {
  t_TRUE : TokenEnum().TRUE,
  t_FALSE : TokenEnum().FALSE
}

def t_IDENTIFIER(t):
  r'(([0-9])|([_A-Za-z]))+'
  if t.value in reserved:
    t.type = reserved[t.value]
  return t

def t_STRINGLIT(t):
  r'[\'"]([^\'^"]*)[\'"]'
  t.value = t.value[1:-1]
  return t

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

def t_error(t):
  print "Illegal character '%s'" % t.value[0]
  t.lexer.skip(1)

lex.lex()
