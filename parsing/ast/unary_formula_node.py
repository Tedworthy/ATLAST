'''
Unary Formula Node
This class implements the AST node of a first order logic formula, in the form
OP formula

Child structure:
  0 = formula
'''

from node import Node

class BinaryFormulaNode(Node):
  _op = None

  # Takes a token from lexer.TokenEnum (unary logical operator, i.e
  # NOT) and a node representing the LHS and the RHS of the formula.
  def __init__(self, op, formula):
    _op = op
    _children[0] = formula

  def getChild():
    return _children[0]
