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

  def getIdentifier(self):
    return self._identifier

  def generateSymbolTable(self, symTable):
    '''
      if variable not exists in symtab:
        add it to top level symtab. unbound.
      else:
        do nothing, it's bound somewhere above us anyway
    '''
    candidate_node = symTable.lookup(self.getIdentifier())
    if candidate_node is None:
        symTable.addGlobal(self._identifier, self)
