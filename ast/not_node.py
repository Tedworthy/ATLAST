'''
Not Node
This class implements the AST node of a first order logic formula, in the form
NOT formula.

Child structure:
  0 = left formula
'''

from unary_formula_node import UnaryFormulaNode

class NotNode(UnaryFormulaNode):
  def __init__(self, node):
    UnaryFormulaNode.__init__(self, node)
