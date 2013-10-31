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

  def generateSymbolTable(symtable):
    if symtable.lookup(_identifier) is None:
      symtable.addGlobal(_identifier, self)

    for child in getChildren():
      child.generateSymbolTable(symtable)
