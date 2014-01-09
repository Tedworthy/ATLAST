'''
If And Only If Node
This class implements the AST node of a first order logic formula, in the form
formula IFF formula.

Child structure:
  0 = left formula
  1 = right formula
'''

from binary_operator_node import BinaryOperatorNode

class IffNode(BinaryOperatorNode):
  def __init__(self, lineNo, position, left, right):
    super(IffNode, self).__init__(lineNo, position, left, right, \
                                  BinaryOperatorNode.IFF)
