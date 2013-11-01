'''
Node
This base class is the basic structure for all nodes in the abstract syntax
tree for our first order logic grammar.
'''

class Node():

  def __init__(self):
    self._children = []
    self._numChildren = 0
    self._symTable = None

  def getChild(self, num):
    if num >= _numChildren:
      raise IndexError("Index", num, "out of bounds in Node.getChild")
    return self._children[num]

  def getChildren(self):
    return self._children

  def setChild(self, num, child):
    self._children.insert(num, child)
    self._numChildren += 1

  def setChildren(self, children):
    self._children = children

  def check():
    raise NotImplementedError("Node.check not implemented!")

  def setSymbolTable(self, symbolTable):
    self._symTable = symbolTable

  def generateSymbolTable(self, symbolTable):
    self._symTable = symbolTable;
    for child in self.getChildren():
      child.generateSymbolTable(symbolTable)

  def __repr__(self):
    return "Class %s with children %s" % (self.__class__, self.getChildren())
