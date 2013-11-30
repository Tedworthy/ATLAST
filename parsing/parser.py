# -*- coding=utf-8 -*-

import ply.yacc as yacc
import sys
import os
from lexer import *
import ast
import error.parser_exceptions as pe
import error.exception_group as eg

precedence = (

  ('left', 'IFF'),
  ('left', 'IMPLIES'),
  ('left', 'OR'),
  ('left', 'AND'),
  ('right', 'NOT'),
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

#Automatically turn A=>B into ~A V B into ~ (A /\ ~ B)
def p_formula_implies(p):
  'formula : formula IMPLIES atomicFormula'
  p[0] =   ast.NotNode(ast.AndNode(p[1],ast.NotNode(p[3])))

### A \/ B ###
def p_formula_or_error_right(p):
  'formula : formula OR error'
  print "Syntax Error in right hand formula"

def p_formula_or_error_left(p):
  'formula : error OR atomicFormula'
  print "Syntax Error in left hand formula"
## using logical equivalence 
## P \/ Q === ~(~P /\ ~Q)
def p_formula_or(p):
  'formula : formula OR atomicFormula'
  p[0] = ast.NotNode(ast.AndNode(ast.NotNode(p[1]), ast.NotNode(p[3])))

### A /\ B ###
def p_formula_and_error_right(p):
  'formula : formula AND error'
  print "Syntax Error: in right hand formula of:\n\t formula AND atomicFormula"

def p_formula_and_error_left(p):
  'formula : error AND atomicFormula'
  print "Syntax Error in left hand formula:\n\t formula AND atomicFormula"

def p_formula_and(p):
  'formula : formula AND formula'
  p[0] = ast.AndNode(p[1], p[3])

### ~ A ###
def p_formula_not_error(p):
  'formula : NOT error'
  print "Syntax Error in Not statement. bad atmoic formula"

def p_formula_not(p):
  'formula : NOT formula '
  print 'Reducing to NOT(' + str(p[2]) + ')'
  p[0] = ast.NotNode(p[2])


#### QUANTIFIER FORMULAS
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
# Creates a shift reduce conflict
# def p_bracketed_atomic_formula(p):
#    'atomicFormula : LBRACKET atomicFormula RBRACKET'
#     p[0] = p[2]

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
  if p is None:
    p.lexer.errors.append(pe.ParserEOIException())
  else:
    last_newline = p.lexer.lexdata.rfind('\n', 0, p.lexer.lexpos)
    last_newline = max(0, last_newline + 1)
    position = p.lexer.lexpos - last_newline + 1 # TODO might be an issue
    p.lexer.errors.append(pe.ParserTokenException(p.lineno, position, \
        unicode(p.value)))

def parse_input(input):
  lexer = getLexer()
  parser = yacc.yacc()
  result = parser.parse(input, lexer)
  if lexer.errors:
    raise eg.ExceptionGroup(lexer.errors)
  return result
