'''
BinaryOperator Node
This class implements an abstract AST node for a binary formula.

Child structure:
  0 = left formula
  1 = right formula
'''

from node import Node

class BinaryOperatorNode(Node):
  EQ = 0
  LT = 1
  LTE = 2
  GT = 3
  GTE = 4
  NEQ = 5
  AND = 6
  OR = 7
  IMPLIES = 8
  IFF = 9
  # Takes two nodes representing the LHS and the RHS of the formula.
  def __init__(self, left, right, op):
    Node.__init__(self)
    self.setChild(0, left)
    self.setChild(1, right)
    self._op = op

  def getLeft(self):
    return Node.getChild(0)

  def getRight(self):
    return Node.getChild(1)

  def getOp(self):
    return self._op
