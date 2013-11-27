'''
Not Node
This class implements the AST node of a first order logic formula, in the form
NOT formula.

Child structure:
  0 = left formula
'''

from unary_operator_node import UnaryOperatorNode

class NotNode(UnaryOperatorNode):
  def __init__(self, node):
    UnaryOperatorNode.__init__(self, node)

  def __repr__(self):
    return 'NOT(' + str(self.getChild(0)) + ')'
