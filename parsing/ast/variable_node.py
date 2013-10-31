'''
Variable Node
This class implements the AST node of a first order logic variable.
'''

from node import Node

class VariableNode(Node):
  _identifier = None

  # Takes a name for the variable.
  def __init__(self, identifier):
    Node.__init__(self)
    _identifier = identifier

  def getIdentifier():
    return _identifier

  def generateSymbolTable(symTable):
    '''
      if variable not exists in symtab:
        add it to top level symtab. unbound.
      else:
        do nothing, it's bound somewhere above us anyway
    '''
    candidate_node = symTable.lookup(_identifier)
    if candidate_node is None:
        symTable.addGlobal(_identifier, self)
