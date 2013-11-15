from ir_node import IRNode

class RelationAliasAttributePair(IRNode):
  def __init__(self, relation, alias, attribute):
    self._relation = relation
    self._attribute = attribute
    self._alias = alias

  def getRelation(self):
    return self._relation

  def getAlias(self):
    return self._alias

  def getAttribute(self):
    return self._attribute

