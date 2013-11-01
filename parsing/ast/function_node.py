'''
Function Node
This class implements the AST node of a first order logic predicate, in the 
form predicate(term_list)

Child structure:
  0..n-1 = List of n terms
'''

from n_arity_application_node import NArityApplicationNode

class FunctionNode(NArityApplicationNode):
  # Takes a list of terms.
  def __init__(self, identifier, terms):
    NArityApplicationNode.__init__(self, identifier)
    _children = terms #TODO refactor

  def getTerm(i):
    return Node.getChild(i)
