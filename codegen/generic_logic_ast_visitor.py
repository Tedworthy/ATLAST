'''
Generic Logic AST Visitor
This class implements the visitor pattern over the AST, converting it to a
generic intermediate representation for code generation.
'''

import visit as v
import ast
from sqlir import SQLIR
from code import web
from copy import copy, deepcopy

class GenericLogicASTVisitor():

  def __init__(self):
    # Instance variables go here, if necessary
    self._IR = SQLIR()
    self._node_stack = []
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
    right_node = self._node_stack.pop()
    left_node = self._node_stack.pop()
    assert left_node
    assert right_node
    assert len(self._node_stack) == 0
    if right_node['type'] == left_node['type'] == 'predicate':
      print 'Both predicate nodes'
      if right_node['table'] == left_node['table']:
        print 'Tables are equal'
        if set(right_node['keys']) == set(left_node['keys']):
          print 'Keys are equal'
    print "And(",left_node,",",right_node,")"
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
    # Iterate over the children from right to left, matching binding values
    binding_values = attributes[1:]
    while len(binding_values) > 0:
      k = binding_values.pop()
      child = self._node_stack.pop()
      if child['type'] == 'variable':
        print "(" + child['node'].getIdentifier() + ", " + k + ")"
        table_attribute = table + '.' + k
        if not child['node'].bindTo(k):
          print 'Could not bind'
          previous_binding = child['node'].boundValue()
          assert previous_binding != None
          self._IR.constraint_stack_conjunction(Constraint(table_attribute,
            previous_binding, '='))
        else:
          print 'Bound'
      else:
        print 'ConstantNode'
    for i in range(0, len(keys)):
      print "Popping", self._node_stack.pop()
    state = {'type' : 'predicate',
             'table' : table,
             'keys' : keys}
    self._node_stack.append(state)
    print self._node_stack

  @v.when(ast.BinaryEqualityNode)
  def visit(self, node):
    print "Seen BinaryEqualityNode"

  @v.when(ast.FunctionNode)
  def visit(self, node):
    print "Seen FunctionNode"

  @v.when(ast.ConstantNode)
  def visit(self, node):
    state = {'type' : 'variable', 'node' : node}
    self._node_stack.append(state)
    print "Seen ConstantNode"

  @v.when(ast.VariableNode)
  def visit(self, node):
    if node.isFree():
      self._IR.addSelectNode(node)  
      print 'Free variable ' , node , ' found'
    state = {'type' : 'variable', 'node' : node}
    self._node_stack.append(state)
    print "Seen VariableNode"

