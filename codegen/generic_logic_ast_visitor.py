'''
Generic Logic AST Visitor
This class implements the visitor pattern over the AST, converting it to a
generic intermediate representation for code generation.
'''

import visit as v
import ast
from codegen.ir import IR
from code import web
from copy import copy, deepcopy
from table_structure import Table

class GenericLogicASTVisitor():

  CROSS_JOIN = 0
  EQUI_JOIN = 1
  NO_JOIN = 2

  def __init__(self):
    # Instance variables go here, if necessary
    self._node_stack = []
    self._IR_stack = []
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
    right_ir = self._IR_stack.pop()
    left_ir = self._IR_stack.pop()
    assert left_node
    assert right_node
    assert len(self._node_stack) == 0
    assert len(self._IR_stack) == 0
    right_keys = right_node['keys']
    left_keys = left_node['keys']
    right_keyvals = right_node['key_values']
    left_keyvals = left_node['key_values']
    # Check the left and right nodes are both predicates
    if right_node['type'] == left_node['type'] == 'predicate':
      print 'Both predicate nodes'
      # Determine if the tables are the same
      if right_node['table'].getIdentifier() == left_node['table'].getIdentifier():
        print 'Tables are equal'
        right_types = [x['type'] for x in right_keyvals]
        left_types = [x['type'] for x in left_keyvals]
        # Check if every element is a variable
        if all(x == 'variable' for x in left_types) \
            and all(x == 'variable' for x in right_types):
          print 'All variables'
          right_ids = [x['node'].getIdentifier() for x in right_keyvals]
          left_ids = [x['node'].getIdentifier() for x in left_keyvals]
          # Finally check if each and every element is the same!
          if right_ids == left_ids:
            # Should push the equal table on to the stack
            self._IR_stack.append(conjunctIR(left_ir, right_ir))
            self._node_stack.append(left_node['table'])
            print 'All ids are the same. TADAAAAAA'
            return
        # Tables are still equal, but elements are not all variables, iterate
        # pairwise through the list.
        print 'Working through constraints'
        constraints_list = []
        for i in range(0, len(right_keyvals)): # TODO: arbitrary - refactor
          left_key = left_keyvals[i]
          right_key = right_keyvals[i]
          if right_key['type'] == left_key['type'] == 'variable':
            if right_key['node'].getIdentifier() == left_key['node'].getIdentifier():
              # Need to add this to the constraint list
              constraint = Constraint(Constraint.EQ,
                  left_key['node'],
                  right_key['node'])
              constraints_list.push(constraint)
              print 'one key was equal!'
            # Bind both of them to the key field
            # i.e node.bindTo(table.attr)
            print 'Bind together variables'
            table_id = left_node['table'].getIdentifier()
            left_key['node'].bindTo(table_id + '.' + left_keys[i])
            right_key['node'].bindTo(table_id + '.' + right_keys[i])
          else:
            print """a mixture of variables and constants found, add some
            constraints"""

    print "And(",left_node,",",right_node,")"

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
    relation = attributes[0]
    # Retrieve the primary keys from the schema
    keys = web.schema.getPrimaryKeys(table)
    # Sort the keys alphabetically as our predicates enforce this
    keys = sorted(keys)
    # Iterate over the children from right to left, matching binding values
    # Python syntax: [1:] ignores first value (index 0), so 1 to end of list.
    binding_values = attributes[1:]
    merged_ir = None
    while len(binding_values) > 0:
      attr = binding_values.pop()
      child = self._node_stack.pop()
      ir = self._IR_stack.pop()
      if child['type'] == 'variable':
        print "(" + child['node'].getIdentifier() + ", " + k + ")"
        rel_attr = RelationAttributePair(relation, attr)
        if not child['node'].bindTo(rel_attr):
          print 'Could not bind'
          previous_binding = child['node'].getBoundValue()
          assert previous_binding != None
          prev_constraints = ir.getConstraintTree()
          new_constraint = Constraint(rel_attr, \
            previous_binding, Constraint.EQ)
          merged_constraint = AndConstraint(prev_constraints, new_constraint)
          ir.setConstraintTree(merged)
        else:
          print 'Now Bound'
      else:
        print 'ConstantNode'
      if merged_ir is not None:
        merged_ir = ir
      else:
        merged_ir = disjunctIR(merged_ir, ir)

    self._IR_stack.append(merged_ir)

    key_values = []
    for i in range(0, len(keys)):
      key_values.append(self._node_stack.pop())
    state = {'type' : 'predicate',
             'table' : Table(table),
             'key_values' : key_values,
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
    state = {'type' : 'constant', 'node' : node}
    self._node_stack.append(state)
    self._IR_stack.append(ir)
    print "Seen ConstantNode"

  @v.when(ast.VariableNode)
  def visit(self, node):
    ir = IR()
    state = {'type' : 'variable', 'node' : node}
    self._node_stack.append(state)
    self._IR_stack.append(ir)
    print "Seen VariableNode"

  def conjunctIR(self, left_ir, right_ir, join_classifier=NO_JOIN, keys=[]):
    rel_attr_pairs = left_ir.getRelationAttributePairs()
    rel_attr_pairs.append(right_ir.getRelationAttributePairs())
    left_ir.setRelationAttributePairs(rel_attr_pairs)

    left_constraints = left_ir.getConstraintTree()
    right_constraints = right_ir.getConstraintTree()
    if constraints is None:
      left_ir.setConstraints(right_constraints)
    elif right_constraints is None:
      left_ir.setConstraints(left_constraints)
    else:
      constraints = AndConstraint(left_constraints, right_ir.getConstraintTree())
      left_ir.setConstraintTree(left_constraints)

    left_relation = left_ir.getRelationTree()
    right_relation = right_ir.getRelationTree()
    if left_relation is None:
      left_ir.setRelationTree(right_relation)
    elif right_relation is None or join_classifier == NO_JOIN:
      left_ir.setRelationTree(left_relation)
    else:
      if join_classifier == EQUI_JOIN:
        relation = EquiJoinNode(left_relation, right_ir.getRelationTree(), keys)
        left_ir.setRelationTree(left_relation)
      elif join_classifier == CROSS_JOIN:
        relation = CrossJoinNode(left_relation, right_ir.getRelationTree(), keys)
        left_ir.setRelationTree(left_relation)

    return left_ir

  def disjunctIR(self, left_ir, right_ir):
    rel_attr_pairs = left_ir.getRelationAttributePairs()
    rel_attr_pairs.append(right_ir.getRelationAttributePairs())
    left_ir.setRelationAttributePairs(rel_attr_pairs)

    left_constraints = left_ir.getConstraintTree()
    right_constraints = right_ir.getConstraintTree()
    if left_constraints is None:
      left_ir.setConstraints(right_constraints)
    elif right_constraints is None:
      left_ir.setConstraints(left_constraints)
    else:
      constraints = OrConstraint(left_constraints, right_ir.getConstraintTree())
      left_ir.setConstraintTree(left_constraints)

    left_relation = left_ir.getRelationTree()
    right_relation = right_ir.getRelationTree()
    if left_relation is None:
      left_ir.setRelationTree(right_relation)
    elif right_relation is None:
      left_ir.setRelationTree(left_relation)
    else:
      print 'You are performing the disjunction of two IRs. You are either\
      crazy, stupid or both'

    return left_ir
