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

  def map_exception_msg(self, x):
    try:
      msg = ' ' + str(x)
    except Exception, e:
      msg = "<unprintable exception", type(e).__name__ + ">"
    return msg

  def __str__(self):
    strings = map(lambda x: self.map_exception_msg(x), self._exceptionList)
    return self.__class__.__name__ + ': [\n' + ',\n'.join(strings) + '\n]'
