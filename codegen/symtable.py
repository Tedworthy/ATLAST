'''
Symbol Table
This class holds data from the abstract syntax tree and creates a table mapping
variable names to nodes and handling scoping.

If parent is None, then this is the top level symbol table.
'''

class SymTable:
  _parent = None
  _data = {}

  def __init__(self, parent=None):
    self._parent = parent

  def getParent(self):
    return self._parent

  def setParent(self, parent):
    self._parent = parent

  def addItem(self, key, value):
    self._data[key] = value

  def hasParent(self):
    return (self._parent is not None)

  def addGlobal(self, key, value):
    if not self.hasParent():
      self.addItem(key, value)
    else:
      getParent().addGlobal(key, value)


  def lookup(self, key):
    # Check for the key in this symbol table
    value = self._data.get(key)
    if value is None:
      # Check for the key in parent symbol table
      if self.hasParent():
        value = self._parent.lookup(key)

    return value
