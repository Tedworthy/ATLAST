'''
BinaryFormula Node
This class implements the AST node of a first order logic formula, in the form
formula OP formula.

Child structure:
  0 = left formula
  1 = right formula
'''

from node import Node

class BinaryFormulaNode(Node):
  _op = None

  # Takes a token from lexer.TokenEnum (binary logical operator, i.e
  # AND, OR, IF, IFF and two nodes representing the LHS and the RHS of the
  # formula.
  def __init__(self, op, left, right):
    _op = op
    _children[0] = left
    _children[1] = right

  def getLeft():
    return _children[0]

  def getRight():
    return _children[1]
