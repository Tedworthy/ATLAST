from ir_node import IRNode

class RelationNode(IRNode):
  def __init__(self, name, alias=None):
    self._name = name
    self._alias = alias

  def getName(self):
    return self._name

  def setAlias(self, alias):
    self._alias = alias

  def getAlias(self):
    if self._alias is None:
      return self.getName()
    else:
      return self._alias

  def hasAlias(self):
    return self._alias is not None;

  def __repr__(self):
    return self.getAlias() + str(id(self))
