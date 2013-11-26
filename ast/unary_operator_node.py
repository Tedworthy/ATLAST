'''
Unary Operator Node
This class implements the AST node of a first order logic formula, in the form
OP formula

Child structure:
  0 = formula
'''

from node import Node

class UnaryOperatorNode(Node):
  # Takes a node representing the RHS of the formula
  def __init__(self, formula):
    Node.__init__(self)
    self.setChild(0, formula)
