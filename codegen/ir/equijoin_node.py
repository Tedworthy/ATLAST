from ir_node import IRNode

class EquiJoinNode(IRNode):
  def __init__(self, left, right, constraint_tree):
    self._left = left
    self._right = right
    self._constraint_tree = constraint_tree

  def getLeft(self):
    return self._left

  def getRight(self):
    return self._right

  def getConstraintTree(self):
    return self._constraint_tree
