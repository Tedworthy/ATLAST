# -*- coding=utf-8 -*-
'''
PARSE TREE -> SQL
This file contains tests for the translation from the parse tree to sql.

NOTE: It assumes that the parser works correctly.
'''
import parsing as p
import codegen.symtable as st
import codegen.ir_generator as irg
import codegen.sql_generator as sg
import semanticanalysis.semantic_analyser as sa
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
    logicTree = p.parse_input(logic)
    print "|*** LOGIC AST ***|\n"
    print str(logicTree)
    # Run dat semantic analysis bro
    dbSchema = schema.Schema()
    semanticAnalyser = sa.SemanticAnalyser(logicTree, dbSchema)
    semanticAnalyser.analyse()

    # Generate the Symbol Table from the Logic Tree
    symbolTable = st.SymTable()
    logicTree.generateSymbolTable(symbolTable)

    # Generate an IR from the Logic Tree (uses Symbol Table)
    irGenerator = irg.IRGenerator(dbSchema)
    logicTree.accept(irGenerator)

    # Pull out the SQL IR
    ir = irGenerator.getIR()

    # Translate the IR to an SQL string
    sqlGenerator = sg.SQLGenerator()
    ir.accept(sqlGenerator)
    translatedSQL = sqlGenerator.getSQL()

    # If the query result does not match the expectation, let the user know.
    if translatedSQL.replace('\n', ' ') != expectedSQL.replace('\n', ' '):
      print "WARNING: Translated SQL does not match the expected result"
      print "Translated SQL: {"
      print translatedSQL
      print "}"
      print "Expected SQL: {"
      print expectedSQL
      print "}"

    # Run translated and expected SQL queries and compare results.
    # Force decode to ASCII as unicode SQL throws a massive wobbly.
    configData = cp.parse_file('dbbackend/db.cfg')
    con = pg.connect(configData)
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
    logic = "∃x(films.title(x, y))".decode('utf-8')
    sql = "SELECT title FROM films"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_two_from_one(self):
    logic = "∃x(films.title(x, y) ∧ films.director(x, z))".decode('utf-8')
    sql = "SELECT title, director FROM films"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_three_from_one(self):
    logic = "∃x(films.title(x, y) ∧ films.director(x, z) ∧ films.made(x, a))".decode('utf-8')
    sql = "SELECT title, director, made FROM films"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_key_from_one(self):
    logic = "films(x)".decode('utf-8')
    sql = "SELECT fid FROM films"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_key_from_one_condition_on_key(self):
    logic = "films(x) ∧ x ≤ 3".decode('utf-8')
    sql = "SELECT fid FROM films WHERE fid <= 3"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_one_from_one_condition_on_one(self):
    logic = "∃x(films.title(x, y) ∧ y = 'The Bourne Identity')".decode('utf-8')
    sql = "SELECT title FROM films WHERE title = 'The Bourne Identity'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_one_from_one_condition_on_one_other(self):
    logic = "∃x(films.title(x, y) ∧ films.origin(x, z) ∧ z = 'US')".decode('utf-8')
    sql = "SELECT title, origin FROM films WHERE origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_two_from_one_condition_on_one(self):
    logic = "∃x(films.title(x, y) ∧ films.origin(x, z) ∧ z = 'US')".decode('utf-8')
    sql = "SELECT title, origin FROM films WHERE origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_two_from_one_condition_on_one_right_literal(self):
    logic = "∃x(films.title(x, y) ∧ films.origin(x, 'US'))".decode('utf-8')
    sql = "SELECT title FROM films WHERE origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_three_from_one_condition_on_two(self):
    logic = "∃x(films.title(x, a) ∧ films.director(x, b) ∧ films.origin(x, c) ∧ a = 'Psycho' ∧ c = 'US')".decode('utf-8')
    sql = "SELECT title, director, origin FROM films WHERE title = 'Psycho' AND origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_three_from_one_condition_on_two_literal(self):
    logic = "∃x(films.title(x, 'Psycho') ∧ films.director(x, b) ∧ films.origin(x, 'US'))".decode('utf-8')
    sql = "SELECT director FROM films WHERE title = 'Psycho' AND origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_two_from_one_condition_on_one_left_literal(self):
    logic = "∃x(films.title(x, 'Ben Hur') ∧ films.director(x, z))".decode('utf-8')
    sql = "SELECT director FROM films WHERE title = 'Ben Hur'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_lt_constraint(self):
    logic = "∃x,z(films.title(x, y) ∧ films.made(x, z) ∧ z < '2002-01-01')".decode('utf-8')
    sql = "SELECT title FROM films WHERE made < '2002-01-01'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_gt_constraint(self):
    logic = "∃x,z(films.title(x, y) ∧ films.made(x, z) ∧ z > '2002-12-31')".decode('utf-8')
    sql = "SELECT title FROM films WHERE made > '2002-12-31'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_gte_constraint(self):
    logic = "∃x,z(films.title(x, y) ∧ films.made(x, z) ∧ z ≥ '2002-01-01')".decode('utf-8')
    sql = "SELECT title FROM films WHERE made >= '2002-01-01'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_lte_constraint(self):
    logic = "∃x,z(films.title(x, y) ∧ films.made(x, z) ∧ z ≤ '2002-12-31')".decode('utf-8')
    sql = "SELECT title FROM films WHERE made <= '2002-12-31'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_eq_constraint(self):
    logic = "∃x,z(films.title(x, y) ∧ films.origin(x, z) ∧ z = 'US')".decode('utf-8')
    sql = "SELECT title FROM films WHERE origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_select_one_condition_on_others(self):
    logic = "∃x,a,c(films.title(x, a) ∧ films.director(x, b) ∧ films.origin(x, c) ∧ a = 'Psycho' ∧ c = 'US')".decode('utf-8')
    sql = "SELECT director FROM films WHERE title = 'Psycho' AND origin = 'US'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  ''' SINGLE TABLE JOINS '''

  @with_setup(setup_func, teardown_func)
  def test_single_table_cross_join_select_one(self):
    logic = "∃x,y,a(films.title(x, a) ∧ films.director(y, b))".decode('utf-8')
    sql = "SELECT films2.director FROM films AS films1 CROSS JOIN films AS films2"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_single_table_cross_join_select_two(self):
    logic = "∃x,y(films.title(x, a) ∧ films.director(y, b))".decode('utf-8')
    sql = "SELECT films1.title, films2.director FROM films AS films1 CROSS JOIN films AS films2"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_single_table_cross_join_select_key(self):
    logic = "∃x(films.title(x, a) ∧ films.director(y, b))".decode('utf-8')
    sql = "SELECT films1.title, films2.fid, films2.director FROM films AS films1 CROSS JOIN films AS films2"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_single_table_cross_join_condition_on_one(self):
    logic = "∃x,y(films.title(x, a) ∧ films.director(y, b) ∧ b = 'Paul Greengrass')".decode('utf-8')
    sql = "SELECT films1.title, films2.director FROM films AS films1 CROSS JOIN films AS films2 WHERE films2.director = 'Paul Greengrass'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_single_table_cross_join_condition_on_two(self):
    logic = "∃x,y(films.title(x, a) ∧ films.director(y, b) ∧ a = 'Ben Hur' ∧ b = 'Paul Greengrass')".decode('utf-8')
    sql = "SELECT films1.title, films2.director FROM films AS films1 CROSS JOIN films AS films2 WHERE films1.title = 'Ben Hur' AND films2.director = 'Paul Greengrass'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_single_table_cross_join_three_times(self):
    logic = "∃x,y,z(films.title(x, a) ∧ films.director(y, b) ∧ films.length(z, c))".decode('utf-8')
    sql = "SELECT films1.title, films2.director, films3.length FROM films AS films1 CROSS JOIN films AS films2 CROSS JOIN films as films3"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_single_table_cross_join_eq(self):
    logic = "∃x,y(films.title(x, a) ∧ films.title(y, b) ∧ a = b)".decode('utf-8')
    sql = "SELECT films1.title, films2.title FROM films AS films1 CROSS JOIN films AS films2 WHERE films1.title = films2.title"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_single_table_cross_join_neq(self):
    logic = "∃x,y(films.title(x, a) ∧ films.title(y, b) ∧ a ≠ b)".decode('utf-8')
    sql = "SELECT films1.title, films2.title FROM films AS films1 CROSS JOIN films AS films2 WHERE films1.title <> films2.title"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  ''' MULTIPLE TABLE JOINS '''

  @with_setup(setup_func, teardown_func)
  def test_join_two_tables(self):
    logic = "∃x(films(x) ∧ casting.fid(y,x))".decode('utf8')
    sql = "SELECT casting.cid FROM films JOIN casting ON films.fid = casting.fid"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_two_table_join_on_field(self):
    logic = "∃x(actors.name(x, z) ∧ casting.aid(y, x))".decode('utf8')
    sql = "SELECT actors.name, casting.cid FROM actors JOIN casting ON actors.aid = casting.aid"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_two_table_join_on_field_order_should_not_matter(self):
    logic = "∃x(casting.aid(y, x) ∧ actors.name(x, z))".decode('utf8')
    sql = "SELECT casting.cid, actors.name FROM actors JOIN casting ON actors.aid = casting.aid"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_two_table_join_on_field_condition_on_one(self):
    logic = "∃x(actors.name(x, 'Matt Damon') ∧ casting.aid(y, x))".decode('utf8')
    sql = "SELECT casting.cid FROM actors JOIN casting ON actors.aid = casting.aid WHERE actors.name = 'Matt Damon'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_two_table_join_on_field_select_three(self):
    logic = "∃x(actors.name(x, z) ∧ casting.aid(y, x) ∧ casting.fid(y, a))".decode('utf8')
    sql = "SELECT actors.name, casting.cid, casting.fid FROM actors JOIN casting ON actors.aid = casting.aid"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_two_table_join_on_field_select_three_order_should_not_matter(self):
    logic = "∃x(casting.fid(y, a) ∧ actors.name(x, z) ∧ casting.aid(y, x))".decode('utf8')
    sql = "SELECT casting.cid, casting.fid, actors.name FROM actors JOIN casting ON actors.aid = casting.aid"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_three_table_join_select_two(self):
    logic = "∃a,c,f(casting.aid(c, a) ∧ casting.fid(c, f) ∧ actors.name(a, aname) ∧ films.title(f, fname))".decode('utf8')
    sql = "SELECT actors.name, films.title FROM casting JOIN actors ON casting.aid = actors.aid JOIN films ON casting.fid = films.fid"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_three_table_join_select_two_rearranged(self):
    logic = "∃a,c,f(casting.aid(c, a) ∧ actors.name(a, aname) ∧ casting.fid(c, f) ∧ films.title(f, fname))".decode('utf8')
    sql = "SELECT actors.name, films.title FROM casting JOIN actors ON casting.aid = actors.aid JOIN films ON casting.fid = films.fid"
    self.translates_to(logic, sql)
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  ''' NEGATIONS '''

  @with_setup(setup_func, teardown_func)
  def test_negate_one_condition(self):
    logic = "∃x(actors.name(x, y) ∧ ¬(y = 'Matt Damon'))".decode('utf8')
    sql = "SELECT actors.name FROM actors WHERE actors.name <> 'Matt Damon'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_negate_one_condition_in_predicate(self):
    logic = "∃x(actors.name(x, y) ∧ ¬actors.name(x, 'Matt Damon'))".decode('utf8')
    sql = "SELECT actors.name FROM actors WHERE actors.name <> 'Matt Damon'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_negate_two_conditions(self):
    logic = "∃x(films.title(x, title) ∧ films.director(x, director) ∧  ¬(director = 'Doug Liman') ∧  ¬(title = 'The Bourne Ultimatum') )".decode('utf8')
    sql = "SELECT films.title, films.director FROM films WHERE NOT(films.director = 'Doug Liman') AND NOT(films.title = 'The Bourne Ultimatum') "
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_negate_two_conditions_in_predicate(self):
    logic = "∃x(films.title(x, title) ∧ films.director(x, director) ∧ ¬(films.director(x, 'Doug Liman')) ∧ ¬(films.title(x, 'The Bourne Ultimatum')) ∧ x ≤ 3)".decode('utf8')
    sql = "SELECT films.title, films.director FROM films WHERE NOT(films.director = 'Doug Liman') AND NOT(films.title = 'The Bourne Ultimatum') AND films.fid <= 3"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_negate_one_relational(self):
    logic = "∃x(films.title(x, title) ∧ ¬(x > 3))".decode('utf8')
    sql = "SELECT films.title FROM films WHERE films.fid <= 3"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  ''' IMPLIES AND IFF '''

  # Query tested in implies form, in or form and conjunctive normal form.
  @with_setup(setup_func, teardown_func)
  def test_implies_simple(self):
    logicImplies = "∃x(¬(films.title(x, y) → films.director(x, 'Ted Sales')))".decode('utf8')
    logicOr      = "∃x(¬(¬films.title(x, y) ∨ films.director(x, 'Ted Sales')))".decode('utf8')
    logicAnd     = "∃x(films.title(x, y) ∧ ¬films.director(x, 'Ted Sales'))".decode('utf8')

    sql = "SELECT films.title FROM films WHERE NOT(films.director = 'Ted Sales')"
    assert self.translates_to(logicImplies, sql), "1) Error, Logic with IMPLIES gives unexpected output."
#    assert self.translates_to(logicOr, sql), "2) Error, Logic using OR gives unexpected output."
#    assert self.translates_to(logicAnd, sql), "3) Error, Logic using neither OR nor IMPLIES gives unexpected output."

  # Query tested in implies form, in or form and conjunctive normal form.
  @with_setup(setup_func, teardown_func)
  def test_iff_simple(self):
    logicImplies = "∃x(¬(films.title(x, y) ↔ films.director(x, 'Ted Sales')))".decode('utf8')
    logicOr      = "∃x(¬((films.title(x, y) ∧ films.director(x, 'Ted Sales')) ∨ (¬films.title(x, y) ∧ ¬films.director(x, 'Ted Sales'))))".decode('utf8')
    logicAnd     = "∃x(¬(films.title(x, y) ∧ films.director(x, 'Ted Sales')) ∧ ¬(¬films.title(x, y) ∧ ¬films.director(x, 'Ted Sales')))".decode('utf8')

    sql = "SELECT films.title FROM films WHERE films.director = 'Ted Sales'"
    assert self.translates_to(logicImplies, sql), "1) Error, Logic with IMPLIES gives unexpected output."
#    assert self.translates_to(logicOr, sql), "2) Error, Logic using OR gives unexpected output."
#    assert self.translates_to(logicAnd, sql), "3) Error, Logic using neither OR nor IMPLIES gives unexpected output."

  ''' Fariba Tests '''
  # These tests come directly from what Fariba got us to type. They are not in any particular order and may be covered by previous tests.

  @with_setup(setup_func, teardown_func)
  def test_fariba_one(self):
    # "Get me all film titles with origin either 'France' or 'Australia'"
    logic = "∃x(films.title(x, y) ∧ (films.origin(x, 'France') ∨ films.origin(x, 'Australia')))".decode('utf8')
    sql = "SELECT films.title FROM films WHERE origin = 'France' OR origin = 'Australia'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  def test_fariba_two(self):
    # "Get me directors with films greater than 100 minutes long."
    logic = "∃x,len(films.director(x, dir) ∧ films.length(x, len) ∧ len > '100')".decode('utf8')
    sql = "SELECT films.director FROM films WHERE films.length > '100'"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  # "Get me directors where all their films are greater than 100 minutes long."
  def test_fariba_three(self):
    logic = "∃x(films.director(x, dir) ∧ ∀y(films.director(y, dir) → (films.length(y, len) ∧ len >'100')))".decode('utf8')
    sql = "SELECT films1.director FROM films AS films1 WHERE NOT EXISTS "
    sql += "(SELECT films2.director FROM films AS films2"
    sql += " WHERE films2.director = films1.director EXCEPT\n"
    sql += "SELECT films2.director FROM films AS films2 WHERE length > '100'"
    sql +=" AND films1.director = films2.director)"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  @with_setup(setup_func, teardown_func)
  # "Get me all actors and the roles they've played."
  def test_fariba_four(self):
    logic = "∃x,a(casting.part(x, y) ∧ casting.aid(x, a) ∧ actors.name(a, b))".decode('utf8')
    sql = "SELECT casting.part, actors.name FROM casting JOIN actors ON casting.aid = actors.aid"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  ''' THERE EXISTS TESTS '''

  @with_setup(setup_func, teardown_func)
  # "Get me all the films such that another film exists, and return that too!."
  def test_there_exists_inner(self):
    logic = "∃x(films.title(x, title1) ∧ ∃y(films.title(y, title2) ∧ title1 ≠ title2))".decode('utf8')
    sql = "SELECT films1.title FROM films AS films1 WHERE EXISTS"
    sql += " (SELECT films2.title FROM films AS films2 WHERE films1.title <> "
    sql += "films2.title)"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  def test_there_exists_inner_negation(self):
    logic = "∃x(films.title(x, title1) ∧ ¬∃y(films.title(y, title2) ∧ title1 ≠ title2))".decode('utf8')
    sql = "SELECT films1.title FROM films AS films1 WHERE EXISTS"
    sql += " (SELECT films2.title FROM films AS films2 WHERE films1.title <> "
    sql += "films2.title)"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  def test_there_exists_inner_negation(self):
    logic = "∃x(films.title(x, title1) ∧ ¬∃y(films.title(y, title2) ∧ title1 ≠ title2))".decode('utf8')
    sql = "SELECT films1.title FROM films AS films1 WHERE EXISTS"
    sql += " (SELECT films2.title FROM films AS films2 WHERE films1.title <> "
    sql += "films2.title)"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"

  def test_there_exists_unification(self):
    logic = "∃x(films.title(x, title1) ∧ ∃y(films.title(y, title) ∧ x ≠ y))".decode('utf8')
    sql = "SELECT films1.title FROM films AS films1 WHERE EXISTS (\n"
    sql += "SELECT films2.title FROM films AS films2 WHERE films1.fid <> films2.fid"
    sql += ")"
    assert self.translates_to(logic, sql), "Error, expected answers not equal"
