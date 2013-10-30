'''
Predicate Node
This class implements the AST node of a first order logic predicate, in the 
form predicate(term_list)

Child structure:
  0..n-1 = List of n terms
'''

from node import Node

class PredicateNode(Node):
  # Takes a list of terms.
  def __init__(self, identifier, terms):
    Node.__init__(self)
    self.setChildren(terms)
