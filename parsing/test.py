from lexer import *
import sys

FORALL = u"\u2200"
AND = u"\u2227"

lex.lex()

if len(sys.argv) > 0:
  input_file = sys.argv[1]
else:
  print "Incorrect usage. try python parser.py [file_name]"
  sys.exit(1)
f = open(input_file, 'r')

lex.input(f.read().decode('utf8'))
while 1:
  tok = lex.token()
  if not tok: break
  print tok
