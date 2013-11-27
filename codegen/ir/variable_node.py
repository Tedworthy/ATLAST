from ir_node import IRNode

class VariableNode(IRNode):
  def __init__(self, string):
    self._identifier = string

  def getIdentifier(self):
    return self._identifier
