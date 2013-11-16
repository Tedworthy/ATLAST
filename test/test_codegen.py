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

    # Run converted and expected SQL queries and compare results.
    # Force decode to ASCII as unicode SQL throws a massive wobbly.
    convertedResult = query.query(convertedSQLString.decode('ascii', 'ignore'))
    expectedResult = query.query(expectedSQLString)

    result = convertedResult == expectedResult
    if not result:
      print convertedResult, "!=", expectedResult

    return result

  ''' SINGLE TABLE QUERIES '''
  
  @with_setup(setup_func, teardown_func)
  def test_select_one_from_one(self):
    logic = "∃x(films_title(x, y))".decode('utf-8')
    sql = "SELECT title FROM films"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_two_from_one(self):
    logic = "∃x(films_title(x, y) ∧ films_director(x, z))".decode('utf8')
    sql = "SELECT title, director FROM films"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_three_from_one(self):
    logic = "∃x(films_title(x, y) ∧ films_director(x, z) ∧ films_made(x, a))".decode('utf8')
    sql = "SELECT title, director, made FROM films"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"
 
  @with_setup(setup_func, teardown_func)
  def test_select_key_from_one(self):
    logic = "films(x)".decode('utf8')
    sql = "SELECT fid FROM films"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_one_from_one_condition_on_one(self):
    logic = "∃x(films_title(x, y) ∧ y = 'The Bourne Identity')".decode('utf8')
    sql = "SELECT title FROM films WHERE title = 'The Bourne Identity'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_one_from_one_condition_on_one_other(self):
    logic = "∃x(films_title(x, y) ∧ films_origin(x, z) ∧ z = 'US')".decode('utf8')
    sql = "SELECT title, origin FROM films WHERE origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_two_from_one_condition_on_one(self):
    logic = "∃x(films_title(x, y) ∧ films_origin(x, z) ∧ z = 'US')".decode('utf8')
    sql = "SELECT title, origin FROM films WHERE origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"
  
  @with_setup(setup_func, teardown_func)
  def test_select_two_from_one_condition_on_one_literal(self):
    logic = "∃x(films_title(x, y) ∧ films_origin(x, 'US'))".decode('utf8')
    sql = "SELECT title FROM films WHERE origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_three_from_one_condition_on_two(self):
    logic = "∃x(films_title(x, a) ∧ films_director(x, b) ∧ films_origin(x, c) ∧ a = 'Psycho' ∧ c = 'US')".decode('utf8')
    sql = "SELECT title, director, origin FROM films WHERE title = 'Psycho' AND origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_three_from_one_condition_on_two_literal(self):
    logic = "∃x(films_title(x, 'Psycho') ∧ films_director(x, b) ∧ films_origin(x, 'US'))".decode('utf8')
    sql = "SELECT director FROM films WHERE title = 'Psycho' AND origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_two_from_one_condition_on_one_literal(self):
    logic = "∃x(films_title(x, 'Ben Hur') ∧ films_director(x, z))".decode('utf8')
    sql = "SELECT director FROM films WHERE title = 'Ben Hur'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_lt_constraint(self):
    logic = "∃x,z(films_title(x, y) ∧ films_made(x, z) ∧ z < '2002-01-01')".decode('utf8')
    sql = "SELECT title FROM films WHERE made < '2002-01-01'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_gt_constraint(self):
    logic = "∃x,z(films_title(x, y) ∧ films_made(x, z) ∧ z > '2002-12-31')".decode('utf8')
    sql = "SELECT title FROM films WHERE made > '2002-12-31'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_gte_constraint(self):
    logic = "∃x,z(films_title(x, y) ∧ films_made(x, z) ∧ z >= '2002-01-01')".decode('utf8')
    sql = "SELECT title FROM films WHERE made >= '2002-01-01'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_lte_constraint(self):
    logic = "∃x,z(films_title(x, y) ∧ films_made(x, z) ∧ z <= '2002-12-31')".decode('utf8')
    sql = "SELECT title FROM films WHERE made <= '2002-12-31'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_eq_constraint(self):
    logic = "∃x,z(films_title(x, y) ∧ films_origin(x, z) ∧ z = 'US')".decode('utf8')
    sql = "SELECT title FROM films WHERE origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_one_condition_on_others(self):
    logic = "∃x,a,c(films_title(x, a) ∧ films_director(x, b) ∧ films_origin(x, c) ∧ a = 'Psycho' ∧ c = 'US')".decode('utf8')
    sql = "SELECT director FROM films WHERE title = 'Psycho' AND origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"
  
  ''' SINGLE TABLE JOINS '''
  
  @with_setup(setup_func, teardown_func)
  def test_single_table_cross_join_select_two(self):
    logic = "∃x,y,a(films_title(x, a) ∧ films_director(y, b))".decode('utf8')
    sql = "SELECT films2.director FROM films AS films1 CROSS JOIN films AS films2"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_single_table_cross_join_select_two(self):
    logic = "∃x,y(films_title(x, a) ∧ films_director(y, b))".decode('utf8')
    sql = "SELECT films1.title, films2.director FROM films AS films1 CROSS JOIN films AS films2"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_single_table_cross_join_select_key(self):
    logic = "∃x(films_title(x, a) ∧ films_director(y, b))".decode('utf8')
    sql = "SELECT films1.title, films2.fid, films2.director FROM films AS films1 CROSS JOIN films AS films2"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_single_table_cross_join_condition_on_one(self):
    logic = "∃x,y(films_title(x, a) ∧ films_director(y, b) ∧ b = 'Paul Greengrass')".decode('utf8')
    sql = "SELECT films1.title, films2.director FROM films AS films1 CROSS JOIN films AS films2 WHERE films2.director = 'Paul Greengrass'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_single_table_cross_join_condition_on_two(self):
    logic = "∃x,y(films_title(x, a) ∧ films_director(y, b) ∧ a = 'Ben Hur' ∧ b = 'Paul Greengrass')".decode('utf8')
    sql = "SELECT films1.title, films2.director FROM films AS films1 CROSS JOIN films AS films2 WHERE films1.title = 'Ben Hur' AND films2.director = 'Paul Greengrass'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"
 
  ''' MULTIPLE TABLE JOINS '''

  @with_setup(setup_func, teardown_func)
  def test_two_table_join_on_field(self):
    logic = "∃x(actors_name(x, z) ∧ casting_aid(y, x))".decode('utf8')
    sql = "SELECT actors.name, casting.cid FROM actors JOIN casting ON actors.aid = casting.aid"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_two_table_join_on_field_order_does_not_matter(self):
    logic = "∃x(casting_aid(y, x) ∧ actors_name(x, z))".decode('utf8')
    sql = "SELECT casting.cid, actors.name FROM actors JOIN casting ON actors.aid = casting.aid"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_two_table_join_on_field_condition_on_one(self):
    logic = "∃x(actors_name(x, 'Matt Damon') ∧ casting_aid(y, x))".decode('utf8')
    sql = "SELECT casting.cid FROM actors JOIN casting ON actors.aid = casting.aid WHERE actors.name = 'Matt Damon'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"
  
  @with_setup(setup_func, teardown_func)
  def test_two_table_join_on_field_select_three(self):
    logic = "∃x(actors_name(x, z) ∧ casting_aid(y, x)) ∧ casting_fid(y, a)".decode('utf8')
    sql = "SELECT actors.name, casting.cid, casting_fid FROM actors JOIN casting ON actors.aid = casting.aid"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

