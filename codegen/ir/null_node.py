from ir_node import IRNode

class NullNode(IRNode):

  def __init__(self):
    self._attribute = 'NULL'
    pass  

  def getAttribute(self):
    return self._attribute

  def getRelation(self):
    return self

  def getAlias(self):
    return self._attribute
