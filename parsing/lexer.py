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
  "OBRACKET",
  "CBRACKET",
  "COMMA",
  "NOT"
  "VARIABLE",
  "CONNECTIVE",
  "FUNCTION",
)

t_FORALL = "∀"
t_THEREEXISTS = "∃"
t_TRUE = "True"
t_FALSE = "False"
t_OR = "|"
t_AND = "&"
t_IMPLIES = "→"
t_IFF = "↔"
t_GT = ">"
t_LT = "<"
t_GTE = "≥"
t_LTE = "≤"
t_EQ = "="
t_OBRACKET = "("
t_CBRACKET = ")"
t_COMMA = ","
t_NOT = "¬"
# One or more lowercase characters
t_VARIABLE = r'[a-z]+'
t_CONNECTIVE = ""
t_FUNCTION = ""

# Variables          -> used in queries 
# Constant Symbols   -> used in declarations
# Functional Symbols -> think addition multiplication subtraction f(x) g(x)
# Relational Symbols -> functions with arities e.g. hasFather(x,y) 
# Logical Constants  -> and|OR| NOT| ForAll| ThereExists| Equal| 
#
