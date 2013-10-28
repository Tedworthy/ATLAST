import ply.yacc as yacc 
import sys
from lexer import tokens

parser = yacc.yacc()

input_file = ''
if sys.argc > 0
  input_file = sys.argv[0]
result = parser(input_file)
