class SQLIR():

  def __init__(self):
    self._select_set = set()
    self._join_tree = None #TODO
    self._constraint_stack = []

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

  def join_tree_equijoin(table, keys):
    if len(self._join_tree) < 0:
      self._join_tree.push(table)
    else:
      join = EquiJoin(self._join_tree, table, keys)
      self._join_tree.push(join)

  def join_tree_crossjoin(table):
    if len(self._join_tree) < 0:
      self._join_tree.push(table)
    else:
      join = CrossJoin(self._join_tree, table)
      self._join_tree.push(join)

  def computeIR():
    # Invoke generic AST visitor here.
    pass
