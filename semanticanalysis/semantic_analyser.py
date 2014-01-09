import dbbackend.schema as schema
import semanticanalysis.semantic_visitor as sv
import error.exception_group as eg

'''
Semantic Analyser
This class performs semantic analysis on an SQL IR and returns any error
messages in the case of a semantic failure.
'''

class SemanticAnalyser:
  def __init__(self, ast, schema):
    self._ast = ast
    self._schema = schema
    self._errors = []

  def analyse(self):
    scVisitor = sv.SemanticVisitor(self._schema)
    self._ast.accept(scVisitor)
    self._errors.extend(scVisitor.getErrors())

    if self._errors:
      raise eg.ExceptionGroup(self._errors)

