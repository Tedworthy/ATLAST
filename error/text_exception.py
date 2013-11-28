class TextException(Exception):

  def __init__(self, lineNo, position):
    self._lineNo = lineNo
    self._position = position

  def getLineNo(self):
    return self._lineNo

  def getPosition(self):
    return self._position

  def __str__(self):
    return 'Line %i, position %i:' % (self._lineNo, self._position)
