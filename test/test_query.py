# -*- coding: utf-8 -*-
from paste.fixture import TestApp
from nose.tools import *
import parsing
from codegen.symtable import SymTable
from codegen.generic_logic_ast_visitor import GenericLogicASTVisitor
from codegen.sql_generator import SQLGenerator

class TestQuery():

  global symbolTable
  symbolTable = None
  global codegenVisitor
  codegenVisitor = None
  global sqlGeneratorVisitor
  qlGeneratorVisitor = None

  def setup_func():
    symbolTable = SymTable()
    codegenVisitor = GenericLogicASTVisitor()
    sqlGeneratorVisitor = SQLGenerator()
    print 'SETUP'

  def teardown_func():
    symbolTable = None
    codegenVisitor = None
    sqlGeneratorVisitor = None

  @with_setup(setup_func, teardown_func)
  def test_two_table_selection_query(self):
    query_string = "∃x(films_title(x, y) ∧ films_director(x, z))".decode('utf8')
    result = parsing.parse_input(query_string)
    # Generate the symbol table
    result.generateSymbolTable(symbolTable)
    # Perform the code generation into SQLIR using the visitor
    result.accept(codegenVisitor)
    codegenVisitor._IR_stack[0].accept(sqlGeneratorVisitor)
    assert_equal(sqlGeneratorVisitor._sql, "")
