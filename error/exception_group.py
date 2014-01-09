class ExceptionGroup(Exception):
  def __init__(self, exceptionList=[]):
    assert exceptionList is not None
    self._exceptionList = exceptionList

  def getExceptionList(self):
    return self._exceptionList

  def addException(self, exception):
    self._exceptionList.append(exception)

  def getDict(self):
    return map(lambda x: x.getDict(), self._exceptionList)

  def __str__(self):
    strings = map(lambda x: '  ' + str(x), self._exceptionList)
    return self.__class__.__name__ + ': [\n' + ',\n'.join(strings) + '\n]'

