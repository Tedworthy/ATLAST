import ply.yacc as yacc 
import sys
import os
from lexer import *
import ast

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

def p_formula_bracketed(p):
  'formula : LBRACKET formula RBRACKET'
  p[0] = p[2]

#Automatically turn A <=> B into (A^B)V(~A^~B) #firstyearlogicbro
def p_formula_iff(p):
  'formula : formula IFF atomicFormula'
  p[0] = ast.OrNode(ast.AndNode(p[1],p[3]),
                    ast.AndNode(ast.NotNode(p[1]),ast.NotNode(p[3])))

#Automatically turn A=>B into ~A V B
def p_formula_implies(p):
  'formula : formula IMPLIES atomicFormula'
  p[0] =  ast.OrNode(ast.NotNode(p[1]),p[3])
#  p[0] = ast.ImpliesNode(p[1], p[3])

def p_formula_or(p):
  'formula : formula OR atomicFormula'
  p[0] = ast.OrNode(p[1], p[3])

def p_formula_and(p):
  'formula : formula AND atomicFormula'
  p[0] = ast.AndNode(p[1], p[3])

def p_formula_not(p):
  'formula : NOT atomicFormula'
  p[0] = ast.NotNode(p[2])

def p_quantifier_list(p):
  'quantifier_list : IDENTIFIER COMMA quantifier_list'
  p[0] = [p[1]] + p[3]

def p_quantifier_single(p):
  'quantifier_list : IDENTIFIER'
  p[0] = [p[1]]

def p_formula_forall(p):
  'formula : FORALL quantifier_list LBRACKET formula RBRACKET'
  p[0] = ast.ForAllNode(p[2], p[4])

def p_formula_thereexists(p):
  'formula : THEREEXISTS quantifier_list LBRACKET formula RBRACKET'
  p[0] = ast.ThereExistsNode(p[2], p[4])

# Atomic Formula grammar

def p_atomic_formula_predicate(p):
  'atomicFormula : IDENTIFIER LBRACKET term_list RBRACKET'
  p[0] = ast.PredicateNode(p[1], p[3])

def p_atomic_formula_eq(p):
  'atomicFormula : term EQ term'
  p[0] = ast.BinaryOperatorNode(p[1], p[3], ast.BinaryOperatorNode.EQ)

def p_atomic_formula_lt(p):
  'atomicFormula : term LT term'
  p[0] = ast.BinaryOperatorNode(p[1], p[3], ast.BinaryOperatorNode.LT)

def p_atomic_formula_lte(p):
  'atomicFormula : term LTE term'
  p[0] = ast.BinaryOperatorNode(p[1], p[3], ast.BinaryOperatorNode.LTE)

def p_atomic_formula_gt(p):
  'atomicFormula : term GT term'
  p[0] = ast.BinaryOperatorNode(p[1], p[3], ast.BinaryOperatorNode.GT)

def p_atomic_formula_gte(p):
  'atomicFormula : term GTE term'
  p[0] = ast.BinaryOperatorNode(p[1], p[3], ast.BinaryOperatorNode.GTE)

def p_atomic_formula_neq(p):
  'atomicFormula : term NEQ term'
  p[0] = ast.BinaryOperatorNode(p[1], p[3], ast.BinaryOperatorNode.NEQ)

# Term list grammar

def p_term_list(p):
  'term_list : term COMMA term_list'
  p[0] = [p[1]] + p[3]

def p_term_list_single(p):
  'term_list : term'
  p[0] = [p[1]]


# Term grammar

def p_term_function(p):
  'term : IDENTIFIER LBRACKET term_list RBRACKET'
  p[0] = ast.FunctionNode(p[1], p[3])

def p_term_constant(p):
  'term : CONSTANT'
  p[0] = ast.ConstantNode(p[1])

def p_term_variable(p):
  'term : IDENTIFIER'
  p[0] = ast.VariableNode(p[1])

def p_term_stringlit(p):
  'term : STRINGLIT'
  print p[1]
  p[0] = ast.StringLitNode(p[1])

# Parsing and error functions

def p_error(p):
  print "Syntax error"

def parse_input(input):
  parser = yacc.yacc()
  result = parser.parse(input)
  return result
