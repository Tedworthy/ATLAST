'''
Variable Node
This class implements the AST node of a first order logic variable.
'''

from node import Node

class VariableNode(Node):
  _identifier = None

  # Takes a name for the variable.
  def __init__(self, identifier):
    Node.__init__(self)
    _identifier = identifier

  def getIdentifier():
    return _identifier

  def generateSymbolTable(symTable):
    symTable.addItem(getIdentifier(), self)
