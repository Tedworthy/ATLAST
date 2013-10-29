'''
BinaryFormula Node
This class implements an abstract AST node for a binary formula.

Child structure:
  0 = left formula
  1 = right formula
'''

from node import Node

class BinaryFormulaNode(Node):
  # Takes two nodes representing the LHS and the RHS of the formula.
  def __init__(self, left, right):
    _children[0] = left
    _children[1] = right

  def getLeft():
    return _children[0]

  def getRight():
    return _children[1]
