'''
Variable Node
This class implements the AST node of a first order logic variable.
'''

from node import Node

class VariableNode(Node):
  _name = None

  # Takes a name for the variable.
  def __init__(self, name):
    Node.__init__(self)
    _name = name

  def getName():
    return _name
