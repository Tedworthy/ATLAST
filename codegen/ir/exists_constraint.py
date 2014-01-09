from unary_constraint import UnaryConstraint

class ExistsConstraint(UnaryConstraint):

  def __init__(self, ir):
    self._ir = ir

  def getIR(self):
    return self._ir

  def __repr__(self):
    return str(self._ir)
