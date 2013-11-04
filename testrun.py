import sys
import parsing
from codegen.symtable import SymTable
from codegen.generic_logic_ast_visitor import GenericLogicASTVisitor

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
result.accept(astVisitor)
