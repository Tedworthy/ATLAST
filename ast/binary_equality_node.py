'''
BinaryEquality Node
This class implements the AST node of a first order logic formula, in the form
formula = formula.
'''

from node import Node

class BinaryEqualityNode(Node):
  def __init__(self, left, right):
    Node.__init__(self)
    self.setChild(0, left)
    self.setChild(1, right)
