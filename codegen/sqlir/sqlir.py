class SQLIR():

  def __init__(self):
    self._select_set = set()
    self._join_tree = None #TODO
    self._constraint_stack = [] #TODO WHY IS THIS A STACK AND NOT A TREE?

  def addSelectNode(self, node):
    self._select_set.add(node)

  def constraint_stack_conjunction(constraint):
    if len(self._constraint_stack) < 0:
      self._constraint_stack.push(constraint)
    else:
      previous_constraint = self._constraint_stack.pop()
      conjunction = AndConstraint(previous_constraint, constraint)

  def constraint_stack_disjunction(constraint):
    if len(self._constraint_stack) < 0:
      self._constraint_stack.push(constraint)
    else:
      previous_constraint = self._constraint_stack.pop()
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

  def computeIR(self):
    # Invoke generic AST visitor here.
    pass

  def accept(self, visitor):
    for select in self._select_set:
      select.accept(self)
    self._join_tree.accept(visitor)
    for constraint in self._constraint_stack:
      constraint.accept(visitor)
    visitor.visit(self)

  def __repr__(self):
    string = "SQLIR: {\n"
    string += "  Select Set: ["
    select_strings = map(str, self._select_set)
    string += ", ".join(select_strings)
    string += "]\n"
    string += "  Join Tree: "
    string += str(self._join_tree)
    string += "\n"
    string += "  Constraint Stack: ["
    constraint_strings = map(str, self._constraint_stack)
    string += ", ".join(constraint_strings)
    string += "]\n"
    string += "}"
    return string
