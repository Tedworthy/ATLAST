from unary_constraint import UnaryConstraint

class DifferenceConstraint(UnaryConstraint):

  def __init__(self, ir, sql_node):
    self._ir = ir
    self._sql_node = sql_node

  def getIR(self):
    return self._ir

  def getSQLNode(self):
    return self._sql_node

  def __repr__(self):
    return str(self._ir)
