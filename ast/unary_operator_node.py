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
  def __init__(self, lineNo, position, formula):
    super(UnaryOperatorNode, self).__init__(lineNo, position)
    self.setChild(0, formula)

  def __repr__(self):
    return 'UnaryOp(' + str(self.getChild(0)) + ')'
