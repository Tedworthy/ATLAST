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
  p[0] = p[1]
  print p[0]

def p_formula_bracketed(p):
  'formula : LBRACKET formula RBRACKET'
  p[0] = 'Bracketed' + p[2]
  print p[0]

def p_formula_iff(p):
  'formula : formula IFF atomicFormula'
  p[0] = "%s iff %s" % (p[1], p[3])
  print p[0]

def p_formula_or(p):
  'formula : formula OR atomicFormula'
  p[0] = "%s or %s" % (p[1], p[3])
  print p[0]

def p_formula_and(p):
  'formula : formula AND atomicFormula'
  p[0] = "%s and %s" % (p[1], p[3])
  print p[0]

def p_formula_not(p):
  'formula : NOT atomicFormula'
  p[0] = 'Negation of an atomicFormula ' + p[2]
  print p[0]

def p_formula_quantifier(p):
  'formula : quantifier IDENTIFIER LBRACKET formula RBRACKET'
  p[0] = p[1] + p[2] + ' for formula ' + p[4]
  print p[0]

# Atomic Formula grammar

def p_atomic_formula_predicate(p):
  'atomicFormula : IDENTIFIER LBRACKET term_list RBRACKET'
  p[0] = 'Predicate %s with terms %s' % (p[1], p[3])

def p_atomic_formula_eq(p):
  'atomicFormula : term EQ term'
  p[0] = '%s equals %s' % (p[1], p[3])

# Term list grammar

def p_term_list(p):
  'term_list : term COMMA term_list'
  p[0] = '%s cons %s' % (p[1], p[3])

def p_term_list_single(p):
  'term_list : term'
  p[0] = p[1]

# Term grammar

def p_term_function(p):
  'term : IDENTIFIER LBRACKET term_list RBRACKET'
  p[0] = 'Function %s with list %s' % (p[1], p[3])

def p_term_constant(p):
  'term : CONSTANT'
  p[0] = p[1]

def p_term_variable(p):
  'term : IDENTIFIER'
  p[0] = p[1]

# Quantifier grammer
def p_quanitifer_forall(p):
  'quantifier : FORALL'
  p[0] = 'FORALL %s' % (p[1])

def p_quanitifer_thereexists(p):
  'quantifier : THEREEXISTS'
  p[0] = 'THEREEXISTS %s' % (p[1])

# Parsing and error functions

def p_error(p):
  print "Syntax error %s" % (p)

if len(sys.argv) > 0:
  input_file = sys.argv[1]
else:
  print "Incorrect usage. try python parser.py [file_name]"
  sys.exit(1)

f = open(input_file, 'r')

parser = yacc.yacc()
result = parser.parse(f.read().decode('utf8'))
