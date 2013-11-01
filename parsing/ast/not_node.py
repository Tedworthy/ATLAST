'''
Not Node
This class implements the AST node of a first order logic formula, in the form
NOT formula.

Child structure:
  0 = left formula
'''

from node import UnaryFormulaNode

class NotNode(UnaryFormulaNode):
  pass
