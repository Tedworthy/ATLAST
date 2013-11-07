'''
Generic Logic AST Visitor
This class implements the visitor pattern over the AST, converting it to a
generic intermediate representation for code generation.
'''

import visit as v
import ast
from sqlir import SQLIR
from code import web

class GenericLogicASTVisitor():

  def __init__(self):
    # Instance variables go here, if necessary
    self._IR = SQLIR()
    self._stack = []
    pass

  @v.on('node')
  def visit(self, node):
    # Generic node, don't think you're supposed to change this
    pass

  @v.when(ast.IffNode)
  def visit(self, node):
    print "Seen IffNode"

  @v.when(ast.OrNode)
  def visit(self, node):
    print "Seen OrNode"

  @v.when(ast.AndNode)
  def visit(self, node):
    print "Seen AndNode"

  @v.when(ast.NotNode)
  def visit(self, node):
    print "Seen NotNode"

  @v.when(ast.ForAllNode)
  def visit(self, node):
    print "Seen ForAllNode"

  @v.when(ast.ThereExistsNode)
  def visit(self, node):
    print "Seen ThereExistsNode"

  @v.when(ast.PredicateNode)
  def visit(self, node):
    # Split out the attributes of the predicate
    attributes = node.getIdentifier().split('_')
    # Get the table name
    table = attributes[0]
    # Retrieve the primary keys from the schema
    keys = web.schema.getPrimaryKeys(table)
    # Sort the keys alphabetically as our predicates enforce this
    keys = sorted(keys)
    # Create a pairwise list mapping the elements in the predicate to their
    # binding values
    keys.extend(attributes[1:])
    # Iterate over the children from right to left, matching binding values
    i = 0
    while len(self._stack) > 0:
      i += 1
      child = self._stack.pop()
      print "(" + child['node'].getIdentifier() + ", " + keys[-1 * i] + ")"

  @v.when(ast.BinaryEqualityNode)
  def visit(self, node):
    print "Seen BinaryEqualityNode"

  @v.when(ast.FunctionNode)
  def visit(self, node):
    print "Seen FunctionNode"

  @v.when(ast.ConstantNode)
  def visit(self, node):
    state = {'type' : 'variable', 'node' : node}
    self._stack.append(state)
    print "Seen ConstantNode"

  @v.when(ast.VariableNode)
  def visit(self, node):
    if node.isFree():
      self._IR.addSelectNode(node)  
      print 'Free variable ' , node , ' found'
    state = {'type' : 'variable', 'node' : node}
    self._stack.append(state)
    print "Seen VariableNode"

