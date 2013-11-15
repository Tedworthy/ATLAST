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

    print logicString

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

    # Run converted and expected SQL queries and compare results

    print convertedSQLString
    print expectedSQLString

    convertedResult = query.query(convertedSQLString)
    expectedResult = query.query(expectedSQLString)

    return convertedResult == expectedResult

  @with_setup(setup_func, teardown_func)
  def test_select_1_from_1(self):
    logic = "∃x(films_title(x, y))".decode('utf-8')
    sql = "SELECT title FROM films"

    assert(self.translates_to(logic, sql))

