# -*- coding=utf-8 -*-
'''
PARSE TREE -> SQL
This file contains tests for the translation from the parse tree to sql.

NOTE: It assumes that the parser works correctly.
'''
import parsing
from codegen.symtable import SymTable
from codegen.generic_logic_ast_visitor import GenericLogicASTVisitor
from codegen.sql_generator import SQLGenerator
import dbbackend.schema as schema
import dbbackend.query as query
from paste.fixture import TestApp
from nose.tools import *

class TestCodeGen():

  def setup_func():
    pass

  def teardown_func():
    pass
  
  def translates_to(self, logicString, expectedSQLString):
    # Create a Logic Tree from the Logic
    logicTree = parsing.parse_input(logicString)

    # Generate the Symbol Table from the Logic Tree
    symbolTable = SymTable()
    logicTree.generateSymbolTable(symbolTable)

    # Generate an AST from the Logic Tree (uses Symbol Table)
    astGenerator = GenericLogicASTVisitor(schema.Schema())
    logicTree.accept(astGenerator)

    # Pull out the SQL IR
    sqlIR = astGenerator.getIR()

    # Convert the IR to an SQL string
    sqlGenerator = SQLGenerator()
    sqlIR.accept(sqlGenerator)
    convertedSQLString = sqlGenerator.getSQL()

    # If the evaluated query does not match the tests expectation, let the user
    # know.
    if convertedSQLString != expectedSQLString:
      print "Potential error: Translated SQL: {"
      print convertedSQLString
      print "}"
      print "does not match expected result: {"
      print expectedSQLString
      print "}"

    # Run converted and expected SQL queries and compare results
    convertedResult = query.query(convertedSQLString)
    expectedResult = query.query(expectedSQLString)

    result = convertedResult == expectedResult
    if not result:
      print "%s != %s", convertedResult, expectedResult

    return result

  @with_setup(setup_func, teardown_func)
  def test_select_single_table(self):
    logic = u"∃x(films_title(x, y))".decode('utf-8')
    sql = "SELECT title FROM films"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_two_from_single_table(self):
    logic = u"∃x(films_title(x, y) ∧ films_director(x, z))".decode('utf8')
    sql = "SELECT title, director FROM films"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_three_from_single_table(self):
    logic = u"∃x(films_title(x, y) ∧ films_director(x, z) ∧ films_made(x, a))".decode('utf8')
    sql = "SELECT title, director, made FROM films"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"
 
  @with_setup(setup_func, teardown_func)
  def test_select_key_from_single_table(self):
    logic = u"films(x)".decode('utf8')
    sql = "SELECT fid FROM films"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_one_from_single_table_condition_on_one_field(self):
    logic = u"∃x(films_title(x, y) ∧ y = 'The Bourne Identity')".decode('utf8')
    sql = "SELECT title FROM films WHERE title = 'The Bourne Identity'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_one_from_single_table_condition_on_other_field(self):
    logic = u"∃x(films_title(x, y) ∧ films_origin(x, z) ∧ z = 'US')".decode('utf8')
    sql = "SELECT title, origin FROM films WHERE origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_two_from_single_table_condition_on_one_field(self):
    logic = u"∃x(films_title(x, y) ∧ films_origin(x, z) ∧ z = 'US')".decode('utf8')
    sql = "SELECT title, origin FROM films WHERE origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"
  
  @with_setup(setup_func, teardown_func)
  def test_select_two_from_single_table_condition_on_one_field_literal(self):
    logic = u"∃x(films_title(x, y) ∧ films_origin(x, 'US'))".decode('utf8')
    sql = "SELECT title, origin FROM films WHERE origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_three_from_single_table_condition_on_two(self):
    logic = u"∃x(films_title(x, a) ∧ films_director(x, b) ∧ films_origin(x, c) ∧ a = 'Psycho' ∧ c = 'US')".decode('utf8')
    sql = "SELECT title, director, origin FROM films WHERE title = 'Psycho' AND origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_three_from_single_table_condition_on_two_literal(self):
    logic = u"∃x(films_title(x, 'Psycho') ∧ films_director(x, b) ∧ films_origin(x, 'US'))".decode('utf8')
    sql = "SELECT title, director, origin FROM films WHERE title = 'Psycho' AND origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_two_from_table_with_stringlit(self):
    logic = u"∃x(films_title(x, 'Ben Hur') ∧ films_director(x, z))".decode('utf8')
    sql = "SELECT director FROM films WHERE title = 'Ben Hur'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_project_lt_constraint(self):
    logic = u"∃x,z(films_title(x, y) ∧ films_made(x, z) ∧ z < '2002-01-01')".decode('utf8')
    sql = "SELECT title FROM films WHERE made < '2002-01-01'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_project_gt_constraint(self):
    logic = u"∃x,z(films_title(x, y) ∧ films_made(x, z) ∧ z > '2002-12-31')".decode('utf8')
    sql = "SELECT title FROM films WHERE made > '2002-12-31'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_project_gte_constraint(self):
    logic = u"∃x,z(films_title(x, y) ∧ films_made(x, z) ∧ z >= '2002-01-01')".decode('utf8')
    sql = "SELECT title FROM films WHERE made >= '2002-01-01'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_project_lte_constraint(self):
    logic = u"∃x,z(films_title(x, y) ∧ films_made(x, z) ∧ z <= '2002-12-31')".decode('utf8')
    sql = "SELECT title FROM films WHERE made <= '2002-12-31'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_project_eq_constraint(self):
    logic = u"∃x,z(films_title(x, y) ∧ films_origin(x, z) ∧ z = 'US')".decode('utf8')
    sql = "SELECT title FROM films WHERE origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_project_two_multiple_constraints(self):
    logic = u"∃x,a,c(films_title(x, a) ∧ films_director(x, b) ∧ films_origin(x, c) ∧ a = 'Psycho' ∧ c = 'US')".decode('utf8')
    sql = "SELECT director FROM films WHERE title = 'Psycho' AND origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_two_table_cross_join(self):
    logic = u"∃x,y(films_title(x, a) ∧ films_director(y, b))".decode('utf8')
    sql = "SELECT films1.title, films2.director FROM films AS films1 CROSS JOIN films AS films2"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

