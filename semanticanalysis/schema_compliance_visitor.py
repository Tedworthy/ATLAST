import dbbackend.schema as schema
import visit as v
import ast

class SchemaComplianceVisitor:
  def __init__(self, schema):
    self._schema = schema
    self._errorLog = "\n  -- Schema Compliance --"
    self._success = True

  @v.on('node')
  def visit(self, node):
    pass

  @v.when(ast.PredicateNode)
  def visit(self, node):
    predicate_name = node.getIdentifier().split('_');
    relation = predicate_name[0]

    if len(predicate_name) > 1:
      attribute = predicate_name[1]
      if not self._schema.relationAttributeExists(relation, attribute):
        self._success = False
        self._errorLog += "\n    Relation '" + relation + "' with attribute '"\
        + attribute + "' does not exist in schema!"
    elif not self._schema.relationExists(relation):
      self._success = False
      self._errorLog += "\n    Relation " +  relation + \
          " does not exist in schema!"


  def getSuccess(self):
    return self._success

  def getErrorLog(self):
    return self._errorLog
