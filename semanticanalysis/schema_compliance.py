import dbbackend.schema as schema
import visit as v
import error.semantic_exceptions as se
import ast

class SchemaCompliance:
  def __init__(self, schema):
    self._schema = schema
    self._errors = []

  def getErrors(self):
    return self._errors

  @v.on('node')
  def visit(self, node):
    pass

  @v.when(ast.PredicateNode)
  def visit(self, node):
    predicate_name = node.getIdentifier().split('_')
    relation = predicate_name[0]

    if len(predicate_name) > 1:
      attribute = predicate_name[1]
      if not self._schema.relationAttributeExists(relation, attribute):
        self._errors.append(se.SemanticSchemaAttributeException( \
            node.getLineNo(), node.getPosition(), relation, attribute))
    elif not self._schema.relationExists(relation):
      self._errors.append(se.SemanticSchemaRelationException( \
          node.getLineNo(), node.getPosition(), relation))

