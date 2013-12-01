from node import Node

class StringLitNode(Node):
  def __init__(self, lineNo, position, value):
    super(StringLitNode, self).__init__(lineNo, position)
    self._value = value

  def getValue(self):
    return self._value

  def __repr__(self):
    return self.getValue()
