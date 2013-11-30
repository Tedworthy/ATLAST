import dbbackend.schema as schema
import semanticanalysis.schema_compliance_visitor as scv

'''
Semantic Analyser
This class performs semantic analysis on an SQL IR and returns any error
messages in the case of a semantic failure.
'''

class SemanticAnalyser:
  def __init__(self, ast, schema):
    self._ast = ast
    self._schema = schema
    self._errorLog = "\n--- Semantic Errors Detected! ---"
    self._success = True

  def analyse(self):
    # Compliance with database schema.
    scVisitor = scv.SchemaComplianceVisitor(self._schema)
    self._ast.accept(scVisitor)
    self._success &= scVisitor.getSuccess();
    self._errorLog += scVisitor.getErrorLog();
    # ... more semantic checks here?

    if not self._success:
      self.raiseErrors()

  def raiseErrors(self):
    raise Exception(self._errorLog)
