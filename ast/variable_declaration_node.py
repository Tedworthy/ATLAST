from node import Node

class VariableDeclarationNode(Node):
  def __init__(self, lineNo, position, symTable):
    super(VariableDeclarationNode, self).__init__(lineNo, position)
    self._symTable = symTable
    self._boundValue = None

  def getBoundValue(self):
    return self._boundValue

  def setBoundValue(self, boundValue):
    self._boundValue = boundValue

  def __repr__(self):
    return str(self.getBoundValue())
