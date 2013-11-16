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
  def __init__(self, left, right):
    BinaryOperatorNode.__init__(self, left, right, BinaryOperatorNode.IMPLIES)
