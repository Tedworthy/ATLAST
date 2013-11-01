import parsing
import codegen
import sys

if len(sys.argv) > 0:
  input_file = sys.argv[1]
else:
  print "Incorrect usage. try python parser.py [file_name]"
  sys.exit(1)

f = open(input_file, 'r')
result = parsing.parse_input(f.read().decode('utf8'))
symbolTable = codegen.SymTable()

# Testing symbol table

result.generateSymbolTable(symbolTable)
print symbolTable

# Testing visitor
