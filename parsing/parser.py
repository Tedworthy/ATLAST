import ply.yacc as yacc 
import sys
from lexer import tokens

precedence = (
  ('left', 'IFF'),
  ('left', 'IMPLIES'),
  ('left', 'OR'),
  ('left', 'AND'),
  ('left', 'NOT'),
)

# Formula grammar

def p_formula_atomic_formula(p):
  'formula : atomicFormula'
  print p[1]

def p_formula_iff(p):
  'formula : formula IFF atomicFormula'
  print "%s iff %s" % p[1], p[3]

def p_formula_or(p):
  'formula : formula OR atomicFormula'
  print "%s or %s" % p[1], p[3]

def p_formula_and(p):
  'formula : formula AND atomicFormula'
  print "%s and %s" % p[1], p[3]

def p_formula_not(p):
  'formula : NOT formula'
  print 'Negation of predicate ' + p[2]

def p_formula_bracketed(p):
  'formula : LBRACKET formula RBRACKET'
  print 'Bracketed' + p[2]

def p_formula_quantifier(p):
  'formula : quantifier formula'
  print 'Quantifier ' + p[1] + ' for formula' + p[2]

# Atomic Formula grammar

def p_atomic_formula_predicate(p):
  'atomicFormula : IDENTIFIER LBRACKET term_list RBRACKET'
  print 'Predicate %s with terms %s' % p[1], p[3]

def p_atomic_formula_eq(p):
  'atomicFormula : term EQ term'
  print '%s equals %s' % p[1], p[3]

# Term list grammar

def p_term_list(p):
  'term_list : term COMMA term_list'
  print 'Term %s cons %s' % p[1], p[3]

def p_term_list_single(p):
  'term_list : term'
  print 'Term %s' % p[1]

# Term grammar

def p_term_function(p):
  'term : IDENTIFIER LBRACKET term_list RBRACKET'
  print 'Function %s with list %s' % p[1], p[3]

def p_term_constant(p):
  'term : CONSTANT'
  print 'Constant %s' % p[1]

def p_term_variable(p):
  'term : IDENTIFIER'
  print 'variable %s' % p[1]

# Quantifier grammer
def p_quanitifer_forall(p):
  'quantifier : FORALL'
  print '%s' % p[1]

def p_quanitifer_thereexists(p):
  'quantifier : THEREEXISTS'
  print '%s' % p[1]

# Parsing and error functions

def p_error(p):
  print "Syntax error"

if len(sys.argv) > 0:
  input_file = sys.argv[1]
else:
  print "Incorrect usage. try python parser.py [file_name]"
  sys.exit(1)

f = open(input_file, 'r')

print f.read()

parser = yacc.yacc()
result = parser(f.read())
