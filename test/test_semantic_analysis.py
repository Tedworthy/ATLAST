# -*- coding=utf-8 -*-
'''
Tests that the semantic analyser picks up semantic errors correctly.

Normal codegen tests (in test_codegen.py) test that errors are not raised when
everything is fine.
'''
import parsing as p
import semanticanalysis.semantic_analyser as sa
import dbbackend.schema as schema
import dbbackend.postgres.postgres_backend as pg

from paste.fixture import TestApp
from nose.tools import *

class TestSemanticAnalysis():

  def __init__(self):
   self._errormsg = "Did not raise expected semantic errors."

  def setup_func(self):
    pass

  def teardown_func(self):
    pass

  def raises_errors(self, logic, expected_errors):
    print 'Logic Recieved: ' + logic
    # Create a Logic Tree from the Logic
    logicTree = p.parse_input(logic)

    # Run dat semantic analysis bro
    dbSchema = schema.Schema()
    semanticAnalyser = sa.SemanticAnalyser(logicTree, dbSchema)

    errors = []
    try:
      semanticAnalyser.analyse()
    except Exception, e:
      errors = e.getDict() # Actually returns list??

    # We don't particularly care about position here; parser tests handle that.
    for error in errors:
      del error["position"]
      del error["line"]

    print error
    print expected_errors
    return sorted(errors) == sorted(expected_errors)

  @with_setup(setup_func, teardown_func)
  def test_invalid_relation(self):
    logic = "TONYFIELD(x)".decode('utf-8')
    errors = [{ "type": "SemanticSchemaRelationException",
                "relation": "TONYFIELD" }]

    assert self.raises_errors(logic, errors), self._errormsg

  @with_setup(setup_func, teardown_func)
  def test_invalid_relation_attr(self):
    logic = "∃x(TONYFIELD.likeshaskell(x, y))".decode('utf-8')
    errors = [{ "type": "SemanticSchemaRelationException",
                "relation": "TONYFIELD" }]
    assert self.raises_errors(logic, errors), self._errormsg

  @with_setup(setup_func, teardown_func)
  def test_invalid_attr(self):
    logic = "∃x(films.boring(x, y))".decode('utf-8')
    errors = [{ "type": "SemanticSchemaAttributeException",
                "relation": "films",
                "attribute": "boring"}]
    assert self.raises_errors(logic, errors), self._errormsg

  @with_setup(setup_func, teardown_func)
  def test_valid_with_invalid_schema(self):
    logic = "∃x,a(films.title(x,y) ∧ tedsales.breakscode(a,z))".decode('utf-8')
    errors = [{ "type": "SemanticSchemaRelationException",
                "relation": "tedsales" }]
    assert self.raises_errors(logic, errors), self._errormsg

  @with_setup(setup_func, teardown_func)
  def test_multiple_schema_errors(self):
    logic = "∃x,a(films.title(x, y) ∧ tedsales.breakscode(a, z)) ∧ \
             suchtestswow(c)".decode('utf-8')
    errors = [{ "type": "SemanticSchemaRelationException",
                "relation": "tedsales" },
              { "type": "SemanticSchemaRelationException",
                "relation": "suchtestswow" }]
    assert self.raises_errors(logic, errors), self._errormsg
