'''
Implies Node
This class implements the AST node of a first order logic formula, in the form
formula IMPLIES formula.

Child structure:
  0 = left formula
  1 = right formula
'''

from node import BinaryFormulaNode

class ImpliesNode(BinaryFormulaNode):
  pass
