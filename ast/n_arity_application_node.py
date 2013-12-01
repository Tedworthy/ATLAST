'''
N Arity Application Node

Base class for a node that applies some method to n arguments (e.g. function
or predicate).
'''

from node import Node

class NArityApplicationNode(Node):
  def __init__(self, lineNo, position, identifier):
    super(NArityApplicationNode, self).__init__(lineNo, position)
    self._identifier = identifier

  def generateSymbolTable(self, symtable):
    self._symtab = symtable
    lookup_result = symtable.lookup(self._identifier)
    if lookup_result is None:
      symtable.addGlobal(self._identifier, self)

    for child in self.getChildren():
      child.generateSymbolTable(symtable)

  def getIdentifier(self):
    return self._identifier
