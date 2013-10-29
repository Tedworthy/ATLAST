'''
And Node
This class implements the AST node of a first order logic formula, in the form
formula AND formula.

Child structure:
  0 = left formula
  1 = right formula
'''

from binary_formula_node import BinaryFormulaNode

class AndNode(BinaryFormulaNode):
  def __init__(self, left, right):
    BinaryFormulaNode.__init__(self, left, right)
