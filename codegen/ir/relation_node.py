from ir_node import IRNode

class RelationNode(IRNode):
  def __init__(self, name):
    self._name = name

  def getName(self):
    return self._name
