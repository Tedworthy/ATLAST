'''
Or Node
This class implements the AST node of a first order logic formula, in the form
formula OR formula.

Child structure:
  0 = left formula
  1 = right formula
'''

from binary_operator_node import *

class OrNode(BinaryOperatorNode):
  def __init__(self, lineNo, position, left, right):
    super(OrNode, self).__init__(lineNo, position, left, right, \
                                 BinaryOperatorNode.OR)
