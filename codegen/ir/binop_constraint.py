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

  def __eq__(self, other):
    if (not isinstance(other, self.__class__)):
      return False
    commutative = (self.getLeftConstraint() == other.getRightConstraint() and
          self.getRightConstraint() == other.getLeftConstraint())
    return (self.getLeftConstraint() == other.getLeftConstraint() and
      self.getRightConstraint() == other.getRightConstraint()) or commutative;

  def __repr__(self):
    string = 'BinOp[]'
    return string
