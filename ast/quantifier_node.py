'''
Quantifier Node
A node representing a quantifier followed by a first order logic formula or
another quantifier node.
'''

from node import *

class QuantifierNode(Node):
  def __init__(self, identifier, formula):
    Node.__init__(self)
    self.setChild(0, formula)
    self._identifier = identifier

  def getIdentifier(self):
    return self._identifier

  def generateSymbolTable(self, symTable):
    print "Adding " + self.getIdentifier() + " to Current Table"
    symTable.addItem(self.getIdentifier(), self)
    childSymbolTable = SymTable(self._symTable)
    print "Child table has parent: " 
    print childSymbolTable.hasParent()
    #### DEBUG ###
    print "Current table: " 
    print symTable
    print "Child table: " 
    print childSymbolTable
    #### DEBUG ###
    
    for child in self.getChildren():
      child.generateSymbolTable(childSymbolTable)


