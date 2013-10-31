'''
Or Node
This class implements the AST node of a first order logic formula, in the form
formula OR formula.

Child structure:
  0 = left formula
  1 = right formula
'''

from binary_formula_node import *

class OrNode(BinaryFormulaNode):
  def __init__(self, left, right):
    BinaryFormulaNode.__init__(self, left, right)
