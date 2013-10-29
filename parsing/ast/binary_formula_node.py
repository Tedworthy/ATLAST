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
    Node.__init__(self)
    setChild(0, left)
    setChild(1, right)

  def getLeft():
    return getChild(0)

  def getRight():
    return getChild(1)
