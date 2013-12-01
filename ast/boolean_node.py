'''
Boolean Node
This class implements the AST node of a first order logic boolean value.
'''

from node import Node

class BooleanNode(Node):

  # Takes a value for the boolean
  def __init__(self, lineNo, position, boolean):
    super(BooleanNode, self).__init__(lineNo, position)
    self._boolean = boolean

  def getBool():
    return self._boolean
