'''
PARSE TREE -> SQL
This file contains tests for the translation from the parse tree to sql.

NOTE: It assumes that the parser works correctly.
'''

import parsing
from paste.fixture import TestApp
from nose.tools import *

class TestCodeGen():

  def setup_func():
    pass

  def teardown_func():
    pass

  @with_setup(setup_func, teardown_func)
  def select_1_from_1(self):
    logic = t_forAll + "x(film_title(x, y))"
    sql = "SELECT title FROM film"
    
    assert(translates_to(logic, sql))


  def translates_to(logicString, expectedSQLString):
    # Create a Logic Tree from the Logic
    logicTree = parsing.parse_input(logicString)

    # Generate an AST from the Logic Tree
    astGenerator = GenericLogicASTVisitor()
    logicTree.accept(astGenerator)

    # Pull out the SQL IR
    sqlIR = astGenerator._IR

    # Convert the IR to an SQL string
    convertedSQLString = SQL_IR_TO_SQL_STRING(sqlIR)
    
    # Run converted and expected SQL queries and compare results
    convertedResult = RUN_SQL(convertedSQLString)
    expectedResult = RUN_SQL(expectedSQLString)

    return convertedResult == expectedResult


