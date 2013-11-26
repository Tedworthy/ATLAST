from ir_node import IRNode

class UnaryConstraint(IRNode):
  def __init__(self,op,child):
    IRNode.__init__(self)
    self._op = op
    self._child = child

  def getConstraint(self):
    return self._child

  def getOp(self):
    return self._op


