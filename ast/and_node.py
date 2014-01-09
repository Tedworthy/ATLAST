'''
And Node
This class implements the AST node of a first order logic formula, in the form
formula AND formula.

Child structure:
  0 = left formula
  1 = right formula
'''

from binary_operator_node import BinaryOperatorNode

class AndNode(BinaryOperatorNode):
  def __init__(self, lineNo, position, left, right):
    super(AndNode, self).__init__(lineNo, position, left, right, \
                                  BinaryOperatorNode.AND)
