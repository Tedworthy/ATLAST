from ir_node import IRNode

class SQLWhereNode(IRNode):

  def __init__(self, ir):
    self._ir = ir

  def getIR(self):
    return self._ir

  def __repr__(self):
    return "SQLWhereNode with IR:" + str(self._ir)
