class SQLIR():

  def __init__(self):
    self._select_set = set()
    self._from_tree = None #TODO
    self._constraint_tree = None #TODO

  def addSelectNode(self, node):
    self._select_set.add(node)

  def computeIR():
    # Invoke generic AST visitor here.
    pass
