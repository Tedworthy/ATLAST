'''
If And Only If Node
This class implements the AST node of a first order logic formula, in the form
formula IFF formula.

Child structure:
  0 = left formula
  1 = right formula
'''

from node import BinaryFormulaNode

class IffNode(BinaryFormulaNode):
  def __init__(self, left, right):
    BinaryFormulaNode.__init__(self, left, right)
