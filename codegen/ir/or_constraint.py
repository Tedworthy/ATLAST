from binop_constraint import *

class OrConstraint(BinOpConstraint):
  def __init__(self, left, right):
    BinOpConstraint.__init__(left, right)
