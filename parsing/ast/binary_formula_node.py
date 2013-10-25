'''
BinaryFormula Node
This class implements the AST node of a first order logic formula, in the form
formula OP formula.

Child structure:
  0 = left formula
  1 = right formula
'''

from node import Node

T_AND = "AND"

class BinaryFormulaNode(Node):
  def setLeftFormula(node):
    _children[0] = node

  def setRightFormula(node):
    _children[1] = node

  def getLeftFormula():
    # TODO array out of bounds checking?
    return _children[0]

  def getRightFormula():
    return _children[1]
