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
    if relationAttributePairs is None:
      print "ASDSADASDASDASDASDASDASDASDASDASDASDASDASDASDA"
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
    print self.getRelationAttributePairs()
    visitor.genSelectNodes(self)
    self._relation_tree.accept(visitor)
    self._constraint_tree.accept(visitor)
    visitor.visit(self)

  def __repr__(self):
    string = "IR = {\n"
    string += "  Relation Attribute Pairs: ["
    string += ", ".join(map(str, self._relation_attribute_pairs))
    string += "]\n"
    string += "  Relation Tree: "
    string += str(self._relation_tree)
    string += "\n"
    string += "  Constraint Tree: "
    string += str(self._constraint_tree)
    string += "\n"
    string += "}"
    return string


''' Things that don't make much sense 

  def constraint_tree_conjunction(constraint):
    if len(self._constraint_tree) < 0:
      self._constraint_tree.push(constraint)
    else:
      previous_constraint = self._constraint_tree.pop()
      conjunction = AndConstraint(previous_constraint, constraint)

  def constraint_tree_disjunction(constraint):
    if len(self._constraint_tree) < 0:
      self._constraint_tree.push(constraint)
    else:
      previous_constraint = self._constraint_tree.pop()
      conjunction = OrConstraint(previous_constraint, constraint)

#  def join_tree_equijoin(table, keys):
#    if len(self._join_tree) < 0:
#      self._join_tree.push(table)
#    else:
#      join = EquiJoin(self._join_tree, table, keys)
#      self._join_tree.push(join)
#
#  def join_tree_crossjoin(table):
#    if len(self._join_tree) < 0:
#      self._join_tree.push(table)
#    else:
#      join = CrossJoin(self._join_tree, table)
#      self._join_tree.push(join)

'''
