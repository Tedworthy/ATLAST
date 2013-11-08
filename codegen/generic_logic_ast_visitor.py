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
    right_keys = right_node['keys']
    left_keys = left_node['keys']
    # Check the left and right nodes are both predicates
    if right_node['type'] == left_node['type'] == 'predicate':
      print 'Both predicate nodes'
      # Determine if the tables are the same
      if right_node['table'] == left_node['table']:
        print 'Tables are equal'
        right_types = [x['type'] for x in right_keys]
        left_types = [x['type'] for x in left_keys]
        # Check if every element is a variable
        if set(right_types) == set(left_types) and right_types[0] == 'variable':
          print 'All variables'
          right_ids = [x['node'].getIdentifier() for x in right_keys]
          left_ids = [x['node'].getIdentifier() for x in left_keys]
          # Finally check if each and every element is the same!
          if right_ids == left_ids:
            # Should push the equal table on to the stack
            print 'All ids are the same. TADAAAAAA'
            return
        # Tables are still equal, but elements are not all variables, iterate
        # pairwise through the list.
        constraint_list = []
        for i in range(0, len(right_keys) - 1):
          left_key = left_keys[i]
          right_key = right_keys[i]
          if right_key['type'] == left_key['type'] == 'variable':
            if right_key['node'].getIdentifier() == left_key['node'].getIdentifier():
              # Need to add this to the constraint list
              print 'one key was equal!'
            # Bind both of them to the key field
            # i.e node.bindTo(table.attr)
            print 'Binding nodes'
          else:
            print """a mixture of variables and constants found, add some
            constraints"""

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
    key_values = []
    for i in range(0, len(keys)):
      key_values.append(self._node_stack.pop())
    state = {'type' : 'predicate',
             'table' : table,
             'keys' : key_values}
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

