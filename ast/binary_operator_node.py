'''
BinaryOperator Node
This class implements an abstract AST node for a binary formula.

Child structure:
  0 = left formula
  1 = right formula
'''

from node import Node

class BinaryOperatorNode(Node):
  # Takes two nodes representing the LHS and the RHS of the formula.
  def __init__(self, left, right):
    Node.__init__(self)
    self.setChild(0, left)
    self.setChild(1, right)

  def getLeft():
    return Node.getChild(0)

  def getRight():
    return Node.getChild(1)
