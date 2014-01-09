'''
There Exists Node
A node representing a 'there exists' quantifier followed by a first order logic 
formula or another quantifier node.
'''

from quantifier_node import QuantifierNode
from variable_declaration_node import VariableDeclarationNode
from node import *

class ThereExistsNode(QuantifierNode):
  def __init__(self, lineNo, position, identifier, formula):
    super(ThereExistsNode, self).__init__(lineNo, position, identifier, formula)
  
  def generateSymbolTable(self, symTable):
    self._symTable = symTable
    for identifier in self.getIdentifiers():
      dec = VariableDeclarationNode(0, 0, symTable)
      symTable.addItem(identifier, dec)
    childSymbolTable = SymTable(symTable)

    for child in self.getChildren():
      child.generateSymbolTable(childSymbolTable)
