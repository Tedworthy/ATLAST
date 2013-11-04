'''
For All Node
A node representing a for all quantifier followed by a first order logic 
formula or another quantifier node.
'''

from quantifier_node import QuantifierNode

class ForAllNode(QuantifierNode):

  def __init__(self, identifier, formula):
    QuantifierNode.__init__(self, identifier, formula)