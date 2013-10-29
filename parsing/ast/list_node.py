'''
Function Node
This class implements the AST node of a first order logic formula.

Child structure:
  0..n-1 = List of n terms
'''

from node import Node

class FunctionNode(Node):
  _identifier = None

  # Takes a string representing the function identifier, and a list of terms.
  def __init__(self, identifier, terms):
    _identifier = name
    _children = terms

  def getTerm(i):
    return _children[i]

  def getIdentifier():
    return _identifier
