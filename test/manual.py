import sys
import os
import parsing
from codegen.symtable import SymTable
from codegen.generic_logic_ast_visitor import GenericLogicASTVisitor
from codegen.sql_generator import SQLGenerator

def print_prefix(message):
  print "[MANUAL]", message

if len(sys.argv) <= 1:
  print "Usage:\n  python {0} <logic_input_file_name>".format(sys.argv[0])
  sys.exit(1)
elif not os.path.exists(sys.argv[1]):
  print "ERROR: Specified file '{0}' does not exist".format(sys.argv[1])
  sys.exit(2)

# Open and display the contents of the input file
f = open(sys.argv[1], 'r')
print_prefix("Logic input:")
f_contents = f.read().decode('utf8')
for line in f_contents.splitlines():
  print_prefix(line)

# Parse the input file
print_prefix("Parsing...")
result = parsing.parse_input(f_contents)

# Print out the generated AST
print_prefix("AST generated:")
print_prefix(result)

# Set up a symbol table and code generation visitor
symbolTable = SymTable()
codegenVisitor = GenericLogicASTVisitor()
sqlGeneratorVisitor = SQLGenerator()

# Generate the symbol table
print_prefix("Generating symbol table...")
result.generateSymbolTable(symbolTable)

# Show the generated symbol table
print_prefix("Symbol table generated:")
print_prefix(symbolTable)

# Perform the code generation into SQLIR using the visitor
print_prefix("Generating SQLIR...")
result.accept(codegenVisitor)

# Print out the IR
print_prefix(codegenVisitor._IR_stack[0])

codegenVisitor._IR_stack[0].accept(sqlGeneratorVisitor)
print_prefix(sqlGeneratorVisitor._sql)
