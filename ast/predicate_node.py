'''
Predicate Node
This class implements the AST node of a first order logic predicate, in the
form predicate(term_list)

Child structure:
  0..n-1 = List of n terms
'''

from n_arity_application_node import NArityApplicationNode

class PredicateNode(NArityApplicationNode):
  # Takes a list of terms.
  def __init__(self, lineNo, position, identifier, terms):
    super(PredicateNode, self).__init__(lineNo, position, identifier)
    self.setChildren(terms)

  def __repr__(self):
      return str(self.getIdentifier()) + "("  + str(self.getChildren()) +  ")"
