'''
Quantifier Node
A node representing a quantifier followed by a first order logic formula or
another quantifier node.
'''

from node import Node

class QuantifierNode(Node):
  def __init__(self, identifier, formula):
    Node.__init__(self)
    self.setChild(0, formula)
    self._identifier = identifier

  def getIdentifier(self):
    return self._identifier

  def generateSymbolTable(self, symTable):
    symTable.addItem(self.getIdentifier(), self)
    childSymbolTable = SymTable(self._symTable)
    for child in self.getChildren():
      child.generateSymbolTable(childSymbolTable)

