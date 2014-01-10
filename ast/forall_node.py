'''
For All Node
A node representing a for all quantifier followed by a first order logic 
formula or another quantifier node.
'''

from quantifier_node import QuantifierNode

class ForAllNode(QuantifierNode):
  def __init__(self, lineNo, position, identifier, formula):
    super(ForAllNode, self).__init__(lineNo, position, identifier, formula)
  def __repr__(self):
      return "\A" + str(self.getIdentifiers()) + "(" + str(self.getChild(0)) +  ")"
