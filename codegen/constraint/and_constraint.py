import BinOpConstraint

class AndConstraint(BinOpConstraint):
  def __init__(self, left, right):
    BinOpConstraint.__init__(left, right)
