from and_constraint import AndConstraint

class IR():

  def __init__(self):
    # An ordered list of field names (strings)
    self._relation_attribute_pairs = []
    # A tree containing the table names and fields to join on.
    self._relation_tree = None
    self._constraint_tree = None
    self._bind_constraint_tree = None

  def getRelationAttributePairs(self):
    return self._relation_attribute_pairs

  def addRelationAttributePair(self, rel_attr):
    for existing in self._relation_attribute_pairs:
      if existing.getRelation().getAlias() == rel_attr.getRelation().getAlias()\
        and existing.getAttribute() == rel_attr.getAttribute():
        return
    self._relation_attribute_pairs.append(rel_attr)

  def addRelationAttributePairs(self, pairs):
    for p in pairs:
      self.addRelationAttributePair(p)

  def setRelationAttributePairs(self, relationAttributePairs):
    self._relation_attribute_pairs = relationAttributePairs;

  def getRelationTree(self):
    return self._relation_tree

  def setRelationTree(self, relationTree):
    self._relation_tree = relationTree

  def getConstraintTree(self):
    return self._constraint_tree

  def setConstraintTree(self, constraintTree):
    self._constraint_tree = constraintTree

  def setBindConstraintTree(self, bindConstraintTree):
    self._bind_constraint_tree = bindConstraintTree

  def getBindConstraintTree(self):
    return self._bind_constraint_tree

  def accept(self, visitor):
    for relAttrPair in self._relation_attribute_pairs:
      relAttrPair.accept(visitor)
    self._relation_tree.accept(visitor)
    if self._constraint_tree is None:
      self._constraint_tree = self._bind_constraint_tree
    if self._constraint_tree is not None:
      if self._bind_constraint_tree is not None:
        self._constraint_tree = AndConstraint(self._constraint_tree,
            self._bind_constraint_tree)
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
    string += "\t\n"
    string += "\t  Bind Constraint Tree: "
    string += str(self._bind_constraint_tree)
    string += "\n"
    string += "\t}"
    return string

