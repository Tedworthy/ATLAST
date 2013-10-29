'''
There Exists Node
A node representing a 'there exists' quantifier followed by a first order logic 
formula or another quantifier node.
'''

from node import QuantifierNode

class ThereExistsNode(QuantifierNode):
  def __init__(self, formula):
    QuantifierNode.__init__(self, formula)
