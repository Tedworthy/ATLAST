from ir_node import IRNode

class RelationAttributePair(IRNode):
  def __init__(self, relation, attribute):
    self._relation = relation
    self._attribute = attribute

  def getRelation(self):
    return self._relation

  def setRelation(self, relation):
    self._relation = relation

  def getAttribute(self):
    return self._attribute

