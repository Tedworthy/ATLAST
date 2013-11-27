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
    print 'Logic Recieved: ' + logic
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
  def test_select_key_from_one_condition_on_key(self):
    logic = "films(x) ∧ x <= 3".decode('utf-8')
    sql = "SELECT fid FROM films WHERE fid <= 3"
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

  @with_setup(setup_func, teardown_func)
  def test_single_table_cross_join_three_times(self):
    logic = "∃x,y,z(films_title(x, a) ∧ films_director(y, b) ∧ films_length(z, c))".decode('utf-8')
    sql = "SELECT films1.title, films2.director, films3.length FROM films AS films1 CROSS JOIN films AS films2 CROSS JOIN films as films3"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  ''' MULTIPLE TABLE JOINS '''

  #MixTutnem
  @with_setup(setup_func, teardown_func)
  def test_join_two_tables(self):
    logic = "∃x(films(x) ∧ casting_fid(y,x))".decode('utf8')
    sql = "SELECT casting.cid FROM films JOIN casting ON films.fid = casting.fid"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_two_table_join_on_field(self):
    logic = "∃x(actors_name(x, z) ∧ casting_aid(y, x))".decode('utf8')
    sql = "SELECT actors.name, casting.cid FROM actors JOIN casting ON actors.aid = casting.aid"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_two_table_join_on_field_order_should_not_matter(self):
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
    logic = "∃x(actors_name(x, z) ∧ casting_aid(y, x) ∧ casting_fid(y, a))".decode('utf8')
    sql = "SELECT actors.name, casting.cid, casting_fid FROM actors JOIN casting ON actors.aid = casting.aid"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_two_table_join_on_field_select_three_order_should_not_matter(self):
    logic = "∃x(casting_fid(y, a) ∧ actors_name(x, z) ∧ casting_aid(y, x))".decode('utf8')
    sql = "SELECT casting.cid, casting_fid, actors.name FROM actors JOIN casting ON actors.aid = casting.aid"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"
  
  @with_setup(setup_func, teardown_func)
  def test_three_table_join_select_two(self):
    logic = "∃x,a,c,f(casting_aid(c, a) ∧ actors_name(a, aname) ∧ casting_fid(c, f) ∧ films_name(f, fname))".decode('utf8')
    sql = "SELECT innerjoin1.name, films.name FROM (casting JOIN actors ON casting.aid = actors.aid) AS innerjoin1 JOIN films ON innerjoin1.fid = films.fid"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  ''' NEGATIONS '''

  @with_setup(setup_func, teardown_func)
  def test_negate_one_condition(self):
    logic = "∃x(actors_name(x, y) ∧ ¬(y = 'Matt Damon'))".decode('utf8')
    sql = "SELECT actors.name FROM actors WHERE actors.name != 'Matt Damon'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_negate_one_condition_in_predicate(self):
    logic = "∃x(actors_name(x, y) ∧ ¬actors_name(x, 'Matt Damon'))".decode('utf8')
    sql = "SELECT actors.name FROM actors WHERE actors.name != 'Matt Damon'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"
  
  @with_setup(setup_func, teardown_func)
  def test_negate_two_conditions(self):
    logic = "∃x(films_title(x, title) ∧ films_director(x, director) ∧  ¬(director = 'Doug Liman') ∧  ¬(title = 'The Bourne Ultimatum') )".decode('utf8')

    sql = "SELECT films.title, films.director FROM films WHERE NOT(films.director = 'Doug Liman') AND NOT(films.title = 'The Bourne Ultimatum') "

    assert self.translates_to(logic, sql), "Error, expected answers not equal"
  
  @with_setup(setup_func, teardown_func)
  def test_negate_two_conditions_in_predicate(self):
    logic = "∃x(films_title(x, title) ∧ films_director(x, director) ∧ ¬(films_director(x, 'Doug Liman')) ∧ ¬(films_title(x, 'The Bourne Ultimatum')) ∧ x <= 3)".decode('utf8')
    sql = "SELECT films.title, films.director FROM films WHERE NOT(films.director = 'Doug Liman') AND NOT(films.title = 'The Bourne Ultimatum') AND films.fid <= 3"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_negate_one_relational(self):
    logic = "∃x(films_title(x, title) ∧ ¬(x > 3))".decode('utf8')
    sql = "SELECT films.title FROM films WHERE films.fid <= 3"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  ''' IMPLIES AND IFF '''

  # Query tested in implies form, in or form and conjunctive normal form.
  @with_setup(setup_func, teardown_func)
  def test_implies_simple(self):

    logic_implies = "∃x(films_title(x, y) →  films_director(x, 'Ted Sales'))".decode('utf8')
#    logic_or      = "∃x(¬(¬films_title(x, y) ∨ films_director(x, 'Ted Sales')))".decode('utf8')
 #   logic_and     = "∃x(films_title(x, y) ∧ ¬films_director(x, 'Ted Sales'))".decode('utf8')
    ##Thats not quite what this logic means in SQL sam, why not start smaller.......

    sql = "SELECT films.title FROM films WHERE films.director = 'Ted Sales'"
    assert self.translates_to(logic_implies, sql), "1) Error, Logic with IMPLIES gives unexpected output."
#    assert self.translates_to(logic_or, sql), "2) Error, Logic using OR gives unexpected output."
 #   assert self.translates_to(logic_and, sql), "3) Error, Logic using neither OR nor IMPLIES gives unexpected output."

  # Query tested in implies form, in or form and conjunctive normal form.
  @with_setup(setup_func, teardown_func)
  def test_iff_simple(self):
    logic_implies = "∃x(¬(films_title(x, y) ↔  films_director(x, 'Ted Sales')))".decode('utf8')
    logic_or      = "∃x(¬((films_title(x, y) ∧ films_director(x, 'Ted Sales')) ∨ (¬films_title(x, y) ∧ ¬films_director(x, 'Ted Sales'))))".decode('utf8')
    logic_and     = "∃x(¬(films_title(x, y) ∧ films_director(x, 'Ted Sales')) ∧ ¬(¬films_title(x, y) ∧ ¬films_director(x, 'Ted Sales')))".decode('utf8')
    sql = "SELECT films.title FROM films WHERE films.director = 'Ted Sales'"
    assert self.translates_to(logic_implies, sql), "1) Error, Logic with IMPLIES gives unexpected output."
#    assert self.translates_to(logic_or, sql), "2) Error, Logic using OR gives unexpected output."
 #   assert self.translates_to(logic_and, sql), "3) Error, Logic using neither OR nor IMPLIES gives unexpected output."


