from node import Node

class StringLitNode(Node):
  def __init__(self, value):
    Node.__init__(self)
    self._value = value

  def getValue(self):
    return self._value
