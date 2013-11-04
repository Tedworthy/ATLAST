 # coding=utf-8
from paste.fixture import TestApp
from nose.tools import *
import parsing
from codegen.symtable import SymTable
from codegen.generic_logic_ast_visitor import GenericLogicASTVisitor
import sys


class TestParser():
  def test_io(self):
    f = open( 'test/input_file.txt', 'r')
    assert_equals(f.read(), '∀x(p(x) ∧ q(x))\n')

  def test_symboltable_generation(self):
    f = open( 'test/input_file.txt', 'r')
    input = f.read().decode('utf8')
    table = SymTable()
    syntax_tree = parsing.parse_input(input)
    syntax_tree.generateSymbolTable(table)
    print table._data['x']
    assert False
    
    
     





'''
if len(sys.argv) > 0:
  input_file = sys.argv[1]
else:
  print "Incorrect usage. try python parser.py [file_name]"
  sys.exit(1)

f = open(input_file, 'r')
result = parsing.parse_input(f.read().decode('utf8'))
symbolTable = SymTable()
astVisitor = GenericLogicASTVisitor()

# Testing symbol table
result.generateSymbolTable(symbolTable)
print symbolTable

# Testing visitor
astVisitor.visit(result)
#result.accept(astVisitor)
'''
