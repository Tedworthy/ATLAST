'''
N Arity Application Node

Base class for a node that applies some method to n arguments (e.g. function
or predicate).
'''

from node import Node

class NArityApplicationNode(Node):
  _identifier = None

  def __init__(self, identifier):
    Node.__init__(self)
    self._identifier = identifier

  def generateSymbolTable(self, symtable):
    if symtable.lookup(self._identifier) is None:
      symtable.addGlobal(self._identifier, self)

    for child in self.getChildren():
      child.generateSymbolTable(symtable)
