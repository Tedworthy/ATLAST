class RelationAttributePair():
  def __init__(self, relation, attribute):
    self._relation = relation
    self._attribute = attribute

  def getRelation(self):
    return self._relation

  def getAttribute(self):
    return self._attribute

