import error.text_exception as te

class LexerException(te.TextException):

  def __init__(self, lineNo, position, character):
    super(LexerException, self).__init__(lineNo, position)
    self._type = self.__class__.__name__
    self._character = character

  def getCharacter(self):
    return self._character

  def __str__(self):
    return super(LexerException, self).__str__() + \
           ' Invalid character \'%s\' encountered' % self._character

  def getDict(self):
    superDict = super(LexerException, self).getDict()
    superDict['character'] = self._character
    superDict['type'] = self._type
    return superDict

