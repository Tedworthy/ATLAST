class IR():

  def __init__(self):
    # An ordered list of field names (strings)
    self._relation_attribute_pairs = []
    # A tree containing the table names and fields to join on.
    self._relation_tree = None
    self._constraint_tree = None

  def getRelationAttributePairs(self):
    return self._relation_attribute_pairs

  def setRelationAttributePairs(self, relationAttributePairs):
    self._relation_attribute_pairs = relationAttributePairs

  def getRelationTree(self):
    return self._relation_tree

  def setRelationTree(self, relationTree):
    self._relation_tree = relationTree

  def getConstraintTree(self):
    return self._constraint_tree

  def setConstraintTree(self, constraintTree):
    self._constraint_tree = constraintTree

  def accept(self, visitor):
    for relAttrPair in self._relation_attribute_pairs:
      relAttrPair.accept(visitor)
    self._relation_tree.accept(visitor)
    if self._constraint_tree is not None:
      self._constraint_tree.accept(visitor)
    visitor.visit(self)

  def __repr__(self):
    string = "IR = {\n"
    string += "\t  Relation Attribute Pairs: ["
    string += '\t, '.join(map(str,self._relation_attribute_pairs))
    string += "\t]\n"
    string += "\t  Relation Tree: "
    string += str(self._relation_tree)
    string += "\t\n"
    string += "\t  Constraint Tree: "
    string += str(self._constraint_tree)
    string += "\n"
    string += "\t}"
    return string

