class CrossJoinNode():
  def __init__(self, left, right):
    self._left = left
    self._right = right

  def getLeft(self):
    return self._left

  def getRight(self):
    return self._right
