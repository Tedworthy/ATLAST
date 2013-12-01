'''
Constant Node
This class implements the AST node of a first order logic constant.
'''

from node import Node

class ConstantNode(Node):

  # Takes a value for the constant.
  def __init__(self, lineNo, position, value):
    super(ConstantNode, self).__init__(lineNo, position)
    self._value = value

  def getValue():
    return self._value
