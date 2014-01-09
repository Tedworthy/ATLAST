'''
Node
This base class is the basic structure for all nodes in the abstract syntax
tree for our first order logic grammar.
'''

from codegen.symtable import SymTable

class Node(object):

  def __init__(self, lineNo, position):
    self._lineNo = lineNo
    self._position = position
    self._children = []
    self._numChildren = 0
    self._symTable = None

  def getLineNo(self):
    return self._lineNo

  def getPosition(self):
    return self._position

  def getChild(self, num):
    if num >= self._numChildren:
      raise IndexError("Index", num, "out of bounds in Node.getChild")
    return self._children[num]

  def getChildren(self):
    return self._children

  def setChild(self, num, child):
    self._children.insert(num, child)
    self._numChildren += 1

  def setChildren(self, children):
    self._children = children

  def setSymbolTable(self, symbolTable):
    self._symTable = symbolTable

  def generateSymbolTable(self, symbolTable):
    self._symTable = symbolTable
    for child in self.getChildren():
      child.generateSymbolTable(symbolTable)

  def accept(self, visitor):
    for child in self.getChildren():
      child.accept(visitor)
    visitor.visit(self)

  def __repr__(self):
    return "Class %s -> %s" % (self.__class__, self.getChildren())
