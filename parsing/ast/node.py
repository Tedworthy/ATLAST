'''
Node
This base class is the basic structure for all nodes in the abstract syntax
tree for our first order logic grammar.
'''

from lexer import TokenEnum

class Node:

  def __init__(self):
    _children = []
    _numChildren = 0

  def getChild(self, num):
    if num >= _numChildren:
      raise IndexError("Index", num, "out of bounds in Node.getChild")
    return _children[num]

  def setChild(self, num, child):
    self._children[num] = child
    self._numChildren += 1

  def check():
    raise NotImplementedError("Node.check not implemented!")
