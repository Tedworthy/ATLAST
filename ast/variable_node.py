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
    attr_eq = True
    rel_eq = True
    resolved_variable_node = self._symTable.lookup(self.getIdentifier())
    if resolved_variable_node.getBoundValue() is None:
      resolved_variable_node.setBoundValue(variable)
    else:
      boundValue = resolved_variable_node._boundValue
      attr_eq = boundValue.getAttribute() == variable.getAttribute()
      rel_eq = boundValue.getRelation().getAlias() == variable.getRelation().getAlias()
    return attr_eq and rel_eq

  def getBoundValue(self):
    resolved_variable_node = self._symTable.lookup(self.getIdentifier())
    return resolved_variable_node._boundValue

  def setBoundValue(self, boundValue):
    self._boundValue = boundValue

  def isFree(self):
    val = self._symTable.lookup(self.getIdentifier())
    # A value is free if, when looking in the symbol table, we find a global
    # variable with no parent (i.e it is at the top level symbol table) or the
    # case in which there is only a symbol table with depth 1. In the latter
    # case, we need to check that the node found is the current node, as in
    # this case the variable must be free (it has not been found quanitified
    # anywhere else).
    return val._symTable.hasParent() or self == val

