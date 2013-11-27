from binop_constraint import BinOpConstraint

class AndConstraint(BinOpConstraint):
  def __init__(self, left, right):
    BinOpConstraint.__init__(self, left, right)

  def __repr__(self):
    return 'AND(' + str(self.getLeftConstraint()) + ',' + str(self.getRightConstraint()) + ')\n'
