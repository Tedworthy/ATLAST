import sys
import os
import parsing
from codegen.symtable import SymTable
from codegen.generic_logic_ast_visitor import GenericLogicASTVisitor

if len(sys.argv) <= 1:
  print "Usage:\n  python {0} <logic_input_file_name>".format(sys.argv[0])
  sys.exit(1)
elif not os.path.exists(sys.argv[1]):
  print "ERROR: Specified file '{0}' does not exist".format(sys.argv[1])
  sys.exit(2)

f = open(sys.argv[1], 'r')
result = parsing.parse_input(f.read().decode('utf8'))
symbolTable = SymTable()
astVisitor = GenericLogicASTVisitor()

# Testing symbol table
result.generateSymbolTable(symbolTable)
print symbolTable

# Testing visitor
result.accept(astVisitor)
