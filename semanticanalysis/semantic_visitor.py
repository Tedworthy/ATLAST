import dbbackend.schema as schema
import visit as v
import error.semantic_exceptions as se
import ast

class SemanticVisitor:
  def __init__(self, schema):
    self._schema = schema
    self._errors = []

  def getErrors(self):
    return self._errors

  def checkRelationAttribute(self, lineno, pos, relation, attribute):
    if not self._schema.relationAttributeExists(relation, attribute):
      e = se.SemanticSchemaAttributeException( \
            lineno, pos, relation, attribute)
      self._errors.append(e)

  def checkRelation(self, lineno, pos, relation):
    if not self._schema.relationExists(relation):
      e = se.SemanticSchemaRelationException(lineno, pos, relation)
      self._errors.append(e)

  @v.on('node')
  def visit(self, node):
    pass

  @v.when(ast.PredicateNode)
  def visit(self, node):
    # Get information about the predicate
    predicate_name = node.getIdentifier().split('.')
    relation = predicate_name[0]
    lineno = node.getLineNo()
    pos = node.getPosition()

    self.checkRelation(lineno, pos, relation)
    # If predicate_name > 1 in length, then it has an attribute.
    # i.e. of the form films_title(x, y) rather than films(x)
    if not self._errors and len(predicate_name) > 1:
      attribute = predicate_name[1]
      self.checkRelationAttribute(lineno, pos, relation, attribute)
