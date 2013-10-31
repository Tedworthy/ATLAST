'''
Constant Node
This class implements the AST node of a first order logic constant.
'''

from node import Node

class ConstantNode(Node):
  _value = None

  # Takes a value for the constant.
  def __init__(self, value):
    Node.__init__(self)
    _value = value

  def getValue():
    return _value
