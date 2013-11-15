'''
PARSE TREE -> SQL
This file contains tests for the translation from the parse tree to sql.

NOTE: It assumes that the parser works correctly.
'''
from parsing import *
from paste.fixture import TestApp
from nose.tools import *

class TestCodeGen():

  def setup_func():
    pass

  def teardown_func():
    pass
  
  def translates_to(self, logicString, expectedSQLString):
    # Create a Logic Tree from the Logic
    logicTree = parse_input(logicString)

    # Generate the Symbol Table from the Logic Tree
    symbolTable = SymTable()
    logicTree.generateSymbolTable(symbolTable)

    # Generate an AST from the Logic Tree (uses Symbol Table)
    astGenerator = GenericLogicASTVisitor()
    logicTree.accept(astGenerator)

    # Pull out the SQL IR
    sqlIR = astGenerator.getIR()

    # Convert the IR to an SQL string
    sqlGenerator = SQLGenerator()
    sqlIR.accept(sqlGenerator)
    convertedSQLString = sqlIR.getSQL()

    # Run converted and expected SQL queries and compare results
    convertedResult = query.query(convertedSQLString)
    expectedResult = query.query(expectedSQLString)

    return convertedResult == expectedResult

  @with_setup(setup_func, teardown_func)
  def test_select_1_from_1(self):
    logic = t_FORALL + "x(film_title(x, y))"
    sql = "SELECT title FROM film"
    
    assert(self.translates_to(logic, sql))

