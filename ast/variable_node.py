'''
Variable Node
This class implements the AST node of a first order logic variable.
'''

from node import Node
from variable_declaration_node import VariableDeclarationNode

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

  #sets self.boundValue to variable and returns True on success
  #if already bound returns false
  def bindTo(self, variable):
    attr_eq = True
    rel_eq = True
    resolved_variable_node = self._symTable.lookup(self.getIdentifier())
    print '***In Bind To ***'
    print '\tVariable is a VariableNode? ' +  str(isinstance(variable,VariableNode)) 
    print '\tResolved_Variable_Node is a VariableNode? ' +  str(isinstance(resolved_variable_node,VariableNode))    
    print '\t' + str(resolved_variable_node)
    

    if resolved_variable_node.getBoundValue() is None:
      resolved_variable_node.setBoundValue(variable)

    #TODO remove this case... its fucked
    elif isinstance(variable,VariableNode) and isinstance(resolved_variable_node, VariableDeclarationNode):
      print 'Dun Bingung de wariable node to de wariable node'
      print '\tValue of variable: ' + variable.getIdentifier()
      print '\tValue of resolved_variable_node: ' + str(resolved_variable_node.getBoundValue().getAttribute())

      resolved_variable_node.setBoundValue(variable)

      
    else:
      boundValue = resolved_variable_node._boundValue
      attr_eq = boundValue.getAttribute() == variable.getAttribute()
      rel_eq = boundValue.getRelation().getAlias() == variable.getRelation().getAlias()
    print '***End Bind To ***'

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

