from ir_node import IRNode

class StringLiteral(IRNode):
  def __init__(self, string):
    self._string = string

  def getString(self):
    return self._string

  def __repr__(self):
    return  "'" + self._string + "'"
