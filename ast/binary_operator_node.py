'''
BinaryOperator Node
This class implements an abstract AST node for a binary formula.

Child structure:
  0 = left formula
  1 = right formula
'''

from node import Node

class BinaryOperatorNode(Node):
  EQ = 0
  LT = 1
  LTE = 2
  GT = 3
  GTE = 4
  NEQ = 5
  AND = 6
  OR = 7
  IMPLIES = 8
  IFF = 9

  op_map = {   0: 'EQ',
               1: 'LT',
               2: 'LTE',
               3: 'GT',
               4: 'GTE',
               5: 'NEQ',
               6: 'AND',
               7: 'OR',
               8: 'IMPLIES',
               9: 'IFF' }
  # Takes two nodes representing the LHS and the RHS of the formula.
  def __init__(self, lineNo, position, left, right, op):
    super(BinaryOperatorNode, self).__init__(lineNo, position)
    self.setChild(0, left)
    self.setChild(1, right)
    self._op = op

  def getLeft(self):
    return self.getChild(0)

  def getRight(self):
    return self.getChild(1)

  def getOp(self):
    return self._op

  def __repr__(self):
    return self.op_map[self.getOp()] + '(' + str(self.getLeft()) + ',' + str(self.getRight()) + ')'
