'''
Node
This base class is the basic structure for all nodes in the abstract syntax
tree for our first order logic grammar.
'''

from lexer import TokenEnum

class Node:
  _children = []
  _numChildren = 0

  def __init__(self):
    pass

  def getChild(num):
    if num >= _numChildren:
      raise IndexError("Index", num, "out of bounds in Node.getChild")
    return _children[num]

  def setChild(num, child):
    _children[num] = child
    _numChildren += 1

  def check():
    raise NotImplementedError("Node.check not implemented!")
