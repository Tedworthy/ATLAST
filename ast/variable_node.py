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

  # NEED TO ADD TO THE SYMBOL TABLE
  def bindTo(self, variable):
    resolved_variable_node = self._symTable.lookup(self.getIdentifier())
    if resolved_variable_node.getBoundValue() is None:
      resolved_variable_node.setBoundValue(variable)
      return True
    return resolved_variable_node._boundValue == variable

  def getBoundValue(self):
    resolved_variable_node = self._symTable.lookup(self.getIdentifier())
    return resolved_variable_node._boundValue

  def setBoundValue(self, boundValue):
    self._boundValue = boundValue

  def isFree(self):
    val = self._symTable.lookup(self.getIdentifier())
    return val._symTable.hasParent()
