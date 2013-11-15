from ir_node import IRNode

class RelationAlias(IRNode):
  def __init__(self, name, alias):
    self._name = name
    self._alias = alias

  def getName(self):
    return self._name

  def getAlias(self):
    return self._alias
