class Table():
  def __init__(self, identifier):
    self.setIdentifier(identifier)

  def getIdentifier(self):
    return self._identifier

  def setIdentifier(self, identifier):
    self._identifier = identifier
