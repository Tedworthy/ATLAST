'''
Quantifier Node
A node representing a quantifier followed by a first order logic formula or
another quantifier node.
'''

from node import Node

class QuantifierNode(Node):
  def __init__(self, formula):
    Node.__init__(self)
    self.setChild(0, formula)
