 # coding=utf-8
from paste.fixture import TestApp
from nose.tools import *

import sys
import parsing as p
import codegen.symtable as st
import codegen.ir_generator as ir

class TestParser():
  def test_io(self):
    f = open('test/input_file.txt', 'r')
    assert_equals(f.read(), '∃x(p(x) ∧ q(x))\n')

  def test_symboltable_generation(self):
    f = open('test/input_file.txt', 'r')
    logic = f.read().decode('utf-8')
    symbolTable = st.SymTable()
    logicAST = p.parse_input(logic)
    logicAST.generateSymbolTable(symbolTable)
    assert_equals(str(symbolTable), 'q,x,p')

