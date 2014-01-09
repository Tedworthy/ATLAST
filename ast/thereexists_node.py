'''
There Exists Node
A node representing a 'there exists' quantifier followed by a first order logic 
formula or another quantifier node.
'''

from quantifier_node import QuantifierNode

class ThereExistsNode(QuantifierNode):
  def __init__(self, lineNo, position, identifier, formula):
    super(ThereExistsNode, self).__init__(lineNo, position, identifier, formula)
