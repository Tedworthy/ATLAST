'''
Variable Node
This class implements the AST node of a first order logic variable.
'''

from node import Node
from variable_declaration_node import VariableDeclarationNode

class VariableNode(Node):
  # Takes a name for the variable.
  def __init__(self, lineNo, position, identifier):
    super(VariableNode, self).__init__(lineNo, position)
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
      print 'Adding global ' + self._identifier
      symTable.addGlobal(self._identifier, self)

  #sets self.boundValue to variable and returns True on success
  #if already bound returns false
  def bindTo(self, variable):
    attr_eq = True
    rel_eq = True
    resolved_variable_node = self._symTable.lookup(self.getIdentifier())
    print '\tVariable is a VariableNode? ' +  str(isinstance(variable,VariableNode)) 
    print '\tResolved_Variable_Node is a VariableNode? ' +  str(isinstance(resolved_variable_node,VariableNode))    
    print '\t' + str(resolved_variable_node)

    if resolved_variable_node.getBoundValue() is None:
      resolved_variable_node.setBoundValue(variable)
    else:
      boundValue = resolved_variable_node.getBoundValue()
      attr_eq = boundValue.getAttribute() == variable.getAttribute()
      rel_eq = boundValue.getRelation() == variable.getRelation()

    return attr_eq and rel_eq

  def getBoundValue(self):
    resolved_variable_node = self._symTable.lookup(self.getIdentifier())
    return resolved_variable_node._boundValue

  def setBoundValue(self, boundValue):
    self._boundValue = boundValue

  def isFree(self):
    val = self._symTable.lookup(self.getIdentifier())
    # The variable is free if we could not find another declaration in the
    # symbol table, or if we did but it was not at global level
    return val._symTable.hasParent() or self == val

  def __repr__(self):
    return self.getIdentifier()
