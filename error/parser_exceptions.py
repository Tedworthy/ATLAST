import error.text_exception as te

class ParserEOIException(Exception):
  def __init__(self):
    pass

  def __str__(self):
    return 'Input finished too soon, maybe you forgot to end a bracket or ' + \
        'quote mark?'

class ParserTokenException(te.TextException):
  def __init__(self, lineNo, position, token):
    super(ParserTokenException, self).__init__(lineNo, position)
    self._token = token
    pass

  def __str__(self):
    return super(ParserTokenException, self).__str__() + \
           ' Unexpected \'%s\'' % self._token

