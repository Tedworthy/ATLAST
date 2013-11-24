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
import dbbackend.postgres.postgres_backend as pg
import dbbackend.config_parser as cp
from paste.fixture import TestApp
from nose.tools import *

class TestCodeGen():

  def setup_func():
    pass

  def teardown_func():
    pass

  def translates_to(self, logic, expectedSQL):
    # Create a Logic Tree from the Logic
    logicTree = parsing.parse_input(logic)

    # Generate the Symbol Table from the Logic Tree
    symbolTable = SymTable()
    logicTree.generateSymbolTable(symbolTable)

    # Generate an IR from the Logic Tree (uses Symbol Table)
    irGenerator = GenericLogicASTVisitor(schema.Schema())
    logicTree.accept(irGenerator)

    # Pull out the SQL IR
    sqlIR = irGenerator.getIR()

    # Translate the IR to an SQL string
    sqlGenerator = SQLGenerator()
    sqlIR.accept(sqlGenerator)
    translatedSQL = sqlGenerator.getSQL()

    # If the query result does not match the expectation, let the user know.
    if translatedSQL != expectedSQL:
      print "WARNING: Translated SQL does not match the expected result"
      print "Translated SQL: {"
      print translatedSQL
      print "}"
      print "Expected SQL: {"
      print expectedSQL
      print "}"

    # Run translated and expected SQL queries and compare results.
    # Force decode to ASCII as unicode SQL throws a massive wobbly.
    config_data = cp.parse_file('dbbackend/db.cfg')
    con = pg.connect(config_data)
    translatedResult = pg.query(con, translatedSQL.decode('ascii', 'ignore'))
    expectedResult = pg.query(con, expectedSQL)
    con.close()
    result = translatedResult == expectedResult
    if not result:
      print translatedResult, " != ", expectedResult

    return result

  ''' SINGLE TABLE QUERIES '''

  @with_setup(setup_func, teardown_func)
  def test_select_one_from_one(self):
    logic = "∃x(films_title(x, y))".decode('utf-8')
    sql = "SELECT title FROM films"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_two_from_one(self):
    logic = "∃x(films_title(x, y) ∧ films_director(x, z))".decode('utf-8')
    sql = "SELECT title, director FROM films"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_three_from_one(self):
    logic = "∃x(films_title(x, y) ∧ films_director(x, z) ∧ films_made(x, a))".decode('utf-8')
    sql = "SELECT title, director, made FROM films"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_key_from_one(self):
    logic = "films(x)".decode('utf-8')
    sql = "SELECT fid FROM films"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_one_from_one_condition_on_one(self):
    logic = "∃x(films_title(x, y) ∧ y = 'The Bourne Identity')".decode('utf-8')
    sql = "SELECT title FROM films WHERE title = 'The Bourne Identity'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_one_from_one_condition_on_one_other(self):
    logic = "∃x(films_title(x, y) ∧ films_origin(x, z) ∧ z = 'US')".decode('utf-8')
    sql = "SELECT title, origin FROM films WHERE origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_two_from_one_condition_on_one(self):
    logic = "∃x(films_title(x, y) ∧ films_origin(x, z) ∧ z = 'US')".decode('utf-8')
    sql = "SELECT title, origin FROM films WHERE origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_two_from_one_condition_on_one_right_literal(self):
    logic = "∃x(films_title(x, y) ∧ films_origin(x, 'US'))".decode('utf-8')
    sql = "SELECT title FROM films WHERE origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_three_from_one_condition_on_two(self):
    logic = "∃x(films_title(x, a) ∧ films_director(x, b) ∧ films_origin(x, c) ∧ a = 'Psycho' ∧ c = 'US')".decode('utf-8')
    sql = "SELECT title, director, origin FROM films WHERE title = 'Psycho' AND origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_three_from_one_condition_on_two_literal(self):
    logic = "∃x(films_title(x, 'Psycho') ∧ films_director(x, b) ∧ films_origin(x, 'US'))".decode('utf-8')
    sql = "SELECT director FROM films WHERE title = 'Psycho' AND origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_two_from_one_condition_on_one_left_literal(self):
    logic = "∃x(films_title(x, 'Ben Hur') ∧ films_director(x, z))".decode('utf-8')
    sql = "SELECT director FROM films WHERE title = 'Ben Hur'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_lt_constraint(self):
    logic = "∃x,z(films_title(x, y) ∧ films_made(x, z) ∧ z < '2002-01-01')".decode('utf-8')
    sql = "SELECT title FROM films WHERE made < '2002-01-01'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_gt_constraint(self):
    logic = "∃x,z(films_title(x, y) ∧ films_made(x, z) ∧ z > '2002-12-31')".decode('utf-8')
    sql = "SELECT title FROM films WHERE made > '2002-12-31'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_gte_constraint(self):
    logic = "∃x,z(films_title(x, y) ∧ films_made(x, z) ∧ z >= '2002-01-01')".decode('utf-8')
    sql = "SELECT title FROM films WHERE made >= '2002-01-01'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_lte_constraint(self):
    logic = "∃x,z(films_title(x, y) ∧ films_made(x, z) ∧ z <= '2002-12-31')".decode('utf-8')
    sql = "SELECT title FROM films WHERE made <= '2002-12-31'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_eq_constraint(self):
    logic = "∃x,z(films_title(x, y) ∧ films_origin(x, z) ∧ z = 'US')".decode('utf-8')
    sql = "SELECT title FROM films WHERE origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_one_condition_on_others(self):
    logic = "∃x,a,c(films_title(x, a) ∧ films_director(x, b) ∧ films_origin(x, c) ∧ a = 'Psycho' ∧ c = 'US')".decode('utf-8')
    sql = "SELECT director FROM films WHERE title = 'Psycho' AND origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  ''' SINGLE TABLE JOINS '''

  @with_setup(setup_func, teardown_func)
  def test_single_table_cross_join_select_one(self):
    logic = "∃x,y,a(films_title(x, a) ∧ films_director(y, b))".decode('utf-8')
    sql = "SELECT films2.director FROM films AS films1 CROSS JOIN films AS films2"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_single_table_cross_join_select_two(self):
    logic = "∃x,y(films_title(x, a) ∧ films_director(y, b))".decode('utf-8')
    sql = "SELECT films1.title, films2.director FROM films AS films1 CROSS JOIN films AS films2"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_single_table_cross_join_select_key(self):
    logic = "∃x(films_title(x, a) ∧ films_director(y, b))".decode('utf-8')
    sql = "SELECT films1.title, films2.fid, films2.director FROM films AS films1 CROSS JOIN films AS films2"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_single_table_cross_join_condition_on_one(self):
    logic = "∃x,y(films_title(x, a) ∧ films_director(y, b) ∧ b = 'Paul Greengrass')".decode('utf-8')
    sql = "SELECT films1.title, films2.director FROM films AS films1 CROSS JOIN films AS films2 WHERE films2.director = 'Paul Greengrass'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_single_table_cross_join_condition_on_two(self):
    logic = "∃x,y(films_title(x, a) ∧ films_director(y, b) ∧ a = 'Ben Hur' ∧ b = 'Paul Greengrass')".decode('utf-8')
    sql = "SELECT films1.title, films2.director FROM films AS films1 CROSS JOIN films AS films2 WHERE films1.title = 'Ben Hur' AND films2.director = 'Paul Greengrass'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

