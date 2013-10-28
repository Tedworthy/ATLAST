'''
Quantifier Node
A node representing a quantifier followed by a first order logic formula or
another quantifier node.
'''

from node import Node

class QuantifierNode(Node):
  _node = None

  # Takes an AST sub node
  def __init__(self, node):
    _node = node

  def getChild():
    return node
