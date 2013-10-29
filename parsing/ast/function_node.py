'''
Function Node
This class implements the AST node of a first order logic predicate, in the 
form predicate(term_list)

Child structure:
  0..n-1 = List of n terms
'''

from node import Node

class FunctionNode(Node):
  # Takes a list of terms.
  def __init__(self, identifier, terms):
    Node.__init__(self)
    _children = terms #TODO refactor

  def getTerm(i):
    return Node.getChild(i)
