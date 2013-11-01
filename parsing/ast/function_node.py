'''
Function Node
This class implements the AST node of a first order logic formula.

Child structure:
  0..n-1 = List of n terms
'''

from node import Node

class FunctionNode(Node):
  _name = None

  # Takes a string representing the function name, and a list of terms.
  def __init__(self, name, terms):
    _name = name
    _children = terms

  def getTerm(i):
    return _children[i]

  def getName():
    return _name
