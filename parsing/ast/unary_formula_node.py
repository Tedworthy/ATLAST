'''
Unary Formula Node
This class implements the AST node of a first order logic formula, in the form
OP formula

Child structure:
  0 = formula
'''

from node import Node

class BinaryFormulaNode(Node):
  # Takes a node representing the RHS of the formula
  def __init__(self, formula):
    _children[0] = formula

  def getChild():
    return _children[0]
