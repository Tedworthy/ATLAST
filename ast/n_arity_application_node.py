'''
N Arity Application Node

Base class for a node that applies some method to n arguments (e.g. function
or predicate).
'''

from node import Node

class NArityApplicationNode(Node):

  def __init__(self, identifier):
    Node.__init__(self)
    self._identifier = identifier

  def generateSymbolTable(self, symtable):
    print "WE GOT CALLED "
    if symtable.lookup(self._identifier) is None:
      symtable.addGlobal(self._identifier, self)

    for child in self.getChildren():
      child.generateSymbolTable(symtable)
