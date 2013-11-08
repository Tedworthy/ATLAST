'''
Variable Node
This class implements the AST node of a first order logic variable.
'''

from node import Node

class VariableNode(Node):
  # Takes a name for the variable.
  def __init__(self, identifier):
    Node.__init__(self)
    self._identifier = identifier
    self._boundValue = None

  def getIdentifier(self):
    return self._identifier

  def generateSymbolTable(self, symTable):
    self._symTable = symTable
    '''
      if variable not exists in symtab:
        add it to top level symtab. unbound.
      else:
        do nothing, it's bound somewhere above us anyway
    '''
    candidate_node = symTable.lookup(self.getIdentifier())
    if candidate_node is None:
        symTable.addGlobal(self._identifier, self)

  def bindTo(self, variable):
    if self._boundValue == None:
      self._boundValue = variable
      return True
    return self._boundValue == variable

  def boundValue(self):
    return self._boundValue

  def isFree(self):
    val = self._symTable.lookup(self.getIdentifier())
    return val._symTable.hasParent()
