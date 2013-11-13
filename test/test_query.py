# -*- coding: utf-8 -*-
from paste.fixture import TestApp
from nose.tools import *
import parsing
from codegen.symtable import SymTable
from codegen.generic_logic_ast_visitor import GenericLogicASTVisitor
from codegen.sql_generator import SQLGenerator
import unittest

class TestQuery(unittest.TestCase):

  def setUp(self):
    self.symbolTable = SymTable()
    self.codegenVisitor = GenericLogicASTVisitor()
    self.sqlGeneratorVisitor = SQLGenerator()

  def setup_func():
    pass

  def teardown_func():
    pass

  @with_setup(setup_func, teardown_func)
  def test_two_table_selection_query(self):
    query_string = "∃x(films_title(x, y) ∧ films_director(x, z))".decode('utf8')
    result = parsing.parse_input(query_string)
    # Generate the symbol table
    result.generateSymbolTable(self.symbolTable)
    # Perform the code generation into SQLIR using the visitor
    result.accept(self.codegenVisitor)
    self.codegenVisitor._IR_stack[0].accept(self.sqlGeneratorVisitor)
    assert_equal(self.sqlGeneratorVisitor._sql, "SELECT films.title, films.director FROM films")
