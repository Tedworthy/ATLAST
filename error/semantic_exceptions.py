import error.text_exception as te

class SemanticSchemaRelationException(te.TextException):
  def __init__(self, lineNo, position, relation):
    super(SemanticSchemaRelationException, self).__init__(lineNo, position)
    self._type = self.__class__.__name__
    self._relation = relation

  def getRelation(self):
    return self._relation

  def __str__(self):
    return super(SemanticSchemaRelationException, self).__str__() + \
        ' Relation \'%s\' does not exist in the database' % self._relation

  def getDict(self):
    superDict = super(SemanticSchemaRelationException, self).getDict()
    superDict['type'] = self._type
    superDict['relation'] = self._relation
    return superDict

class SemanticSchemaAttributeException(te.TextException):
  def __init__(self, lineNo, position, relation, attribute):
    super(SemanticSchemaAttributeException, self).__init__(lineNo, position)
    self._type = self.__class__.__name__
    self._relation = relation
    self._attribute = attribute

  def getRelation(self):
    return self._relation

  def getAttribute(self):
    return self._attribute

  def __str__(self):
    return super(SemanticSchemaAttributeException, self).__str__() + \
        ' Relation \'%s\' with attribute \'%s\' does not exist in the database'\
        % (self._relation, self._attribute)

  def getDict(self):
    superDict = super(SemanticSchemaAttributeException, self).getDict()
    superDict['type'] = self._type
    superDict['relation'] = self._relation
    superDict['attribute'] = self._attribute
    return superDict

