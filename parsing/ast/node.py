'''
Node
This base class is the basic structure for all nodes in the abstract syntax
tree for our first order logic grammar.
'''

from lexer import TokenEnum

class Node():

  def __init__(self):
    self._children = []
    self._numChildren = 0

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

  def __repr__(self):
    return "Class %s with children %s" % (self.__class__, self.getChildren())
