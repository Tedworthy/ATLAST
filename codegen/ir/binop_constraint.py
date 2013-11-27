from ir_node import IRNode

class BinOpConstraint(IRNode):
  def __init__(self, left, right):
    IRNode.__init__(self)
    self._left = left
    self._right = right

  def getLeftConstraint(self):
    return self._left

  def getRightConstraint(self):
    return self._right

  def __repr__(self):
    string = 'BinOp[]'
    return string
