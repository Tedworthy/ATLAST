'''
Implies Node
This class implements the AST node of a first order logic formula, in the form
formula IMPLIES formula.

Child structure:
  0 = left formula
  1 = right formula
'''

from binary_operator_node import BinaryOperatorNode

class ImpliesNode(BinaryOperatorNode):
  def __init__(self, lineNo, position, left, right):
    super(ImpliesNode, self).__init__(lineNo, position, left, right, \
                                      BinaryOperatorNode.IMPLIES)
