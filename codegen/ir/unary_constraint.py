from ir_node import IRNode

class UnaryConstraint(IRNode):
  def __init__(self,op,child):
    IRNode.__init__(self)
    self.op = op
    self._child = child

  def getConstraint(self):
    return self._child

