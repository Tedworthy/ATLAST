'''
Unary Formula Node
This class implements the AST node of a first order logic formula, in the form
OP formula

Child structure:
  0 = formula
'''

from node import Node

class UnaryFormulaNode(Node):
  # Takes a node representing the RHS of the formula
  def __init__(self, formula):
    setFormula(formula)

  def setFormula(formula):
    Node.setChild(0, formula)

