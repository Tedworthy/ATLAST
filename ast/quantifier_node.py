'''
Quantifier Node
A node representing a quantifier followed by a first order logic formula or
another quantifier node.
'''

from node import *
from variable_declaration_node import VariableDeclarationNode

class QuantifierNode(Node):
  def __init__(self, identifiers, formula):
    Node.__init__(self)
    self.setChild(0, formula)
    self._identifiers = identifiers
    self._boundValue = None

  def getBoundValue(self):
    return self._boundValue

  def setBoundValue(self, boundValue):
    self._boundValue = boundValue

  def getIdentifiers(self):
    return self._identifiers

  def generateSymbolTable(self, symTable):
    self._symTable = symTable
    for identifier in self.getIdentifiers():
      dec = VariableDeclarationNode(symTable)
      symTable.addItem(identifier, dec)
    childSymbolTable = SymTable(symTable)

    for child in self.getChildren():
      child.generateSymbolTable(childSymbolTable)


