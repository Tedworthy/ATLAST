import error.text_exception as te

class ParserEOIException(Exception):
  def __init__(self):
    self._type = self.__class__.__name__

  def __str__(self):
    return 'Input finished too soon, maybe you forgot to end a bracket or ' + \
        'quote mark?'

  def getDict(self):
    return {
        'type': self._type
      }

class ParserTokenException(te.TextException):
  def __init__(self, lineNo, position, token):
    super(ParserTokenException, self).__init__(lineNo, position)
    self._type = self.__class__.__name__
    self._token = token

  def __str__(self):
    return super(ParserTokenException, self).__str__() + \
           ' Unexpected \'%s\'' % self._token

  def getDict(self):
    superDict = super(ParserTokenException, self).getDict()
    superDict['token'] = self._token
    superDict['type'] = self._type
    return superDict

