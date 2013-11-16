from node import Node

class VariableDeclarationNode(Node):
  def __init__(self, symTable):
    Node.__init__(self)
    self._symTable = symTable
    self._boundValue = None

  def getBoundValue(self):
    return self._boundValue

  def setBoundValue(self, boundValue):
    self._boundValue = boundValue
