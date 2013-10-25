import ply.yacc as yacc 
import sys
from lexer import tokens


if len(sys.argv) > 0:
  input_file = sys.argv[1]
else:
  print "Incorrect usage. try python parser.py [file_name]"
  sys.exit(1)

f = open(input_file, 'r')

print f.read()

parser = yacc.yacc()
result = parser(f.read())
