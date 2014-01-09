from ir_node import IRNode

class Constant(IRNode):
  def __init__(self, value):
    self._value = value

  def getValue(self):
    return self._value

  def __repr__(self):
    return str(self._value)
