'''
Symbol Table
This class traverses the abstract syntax tree and creates a table mapping
variable names to nodes and handling scoping. A symbol table may contain
a parent and any number of child symbol tables.

If parent is None, then this is the top level symbol table.
'''

class SymTable:
  _parent = None
  _children = []
  _data = {}

  def __init__(self, parent=None):
    pass




