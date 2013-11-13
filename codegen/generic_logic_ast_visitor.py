'''
Generic Logic AST Visitor
This class implements the visitor pattern over the AST, converting it to a
generic intermediate representation for code generation.
'''

import visit as v
import ast
from codegen.ir import *
from code import web
from copy import copy, deepcopy

class GenericLogicASTVisitor():

  CROSS_JOIN = 0
  EQUI_JOIN = 1
  NO_JOIN = 2

  def __init__(self):
    # Instance variables go here, if necessary
    self._node_stack = []
    self._IR_stack = []

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
    print self._IR_stack
    assert len(self._IR_stack) == 0
    right_keys = right_node['keys']
    left_keys = left_node['keys']
    right_keyvals = right_node['key_values']
    left_keyvals = left_node['key_values']
    # Check the left and right nodes are both predicates
    if right_node['type'] == left_node['type'] == 'predicate':
      print 'Both predicate nodes'
      # Determine if the tables are the same
      if right_node['table'] == left_node['table']:
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
            ir = self.conjunctIR(left_ir, right_ir)
            ir.setRelationTree(RelationNode(left_node['table']))
            self._IR_stack.append(ir)
            self._node_stack.append(left_node['table'])
            print 'All keys are the same. TADAAAAAA'
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
              left_rel_attr = RelationAttributePair(left_node['table'], left_key['node'])
              right_rel_attr = RelationAttributePair(right_node['table'], right_key['node'])
              constraint = Constraint(Constraint.EQ, left_rel_attr, right_rel_attr)
              constraints_list.push(constraint) ########################################## TODO TODO WHADDAYA DO WITH DEM CONSTRAINTS BRO?
              print 'one key was equal!'
            # Bind both of them to the key field
            # i.e node.bindTo(table.attr)
            print 'Bind together variables'
            table_id = left_node['table'].getIdentifier()
            left_key['node'].bindTo(table_id + '.' + left_keys[i]) ############################### TODO TODO TODO PROBABLY BOLLOCKS
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
    keys = web.schema.getPrimaryKeys(relation)
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
        print "(" + child['node'].getIdentifier() + ", " + attr + ")"
        rel_attr = RelationAttributePair(relation, attr)
        if child['node'].isFree():
          ir.setRelationAttributePairs([rel_attr])
        if not child['node'].bindTo(rel_attr):
          print 'Could not bind'
          print 'its the top one'
          print child['node'].getBoundValue()
          previous_binding = child['node'].getBoundValue()
          assert previous_binding != None
          prev_constraints = ir.getConstraintTree()
          new_constraint = Constraint(Constraint.EQ, rel_attr, \
            previous_binding)
          merged_constraint = None;
          if prev_constraints is None:
            ir.setConstraintTree(new_constraint)
          elif new_constraint is None:
            ir.setConstraintTree(prev_constraints)
          else:
            merged_constraint = AndConstraint(prev_constraints, new_constraint)
            ir.setConstraintTree(merged_constraint)
        else:
          print 'Now Bound'
      else:
        print 'ConstantNode'
      if merged_ir is None:
        merged_ir = ir
      else:
        merged_ir = self.conjunctIR(merged_ir, ir)

    key_values = []
    for i in range(0, len(keys)):
      ir = self._IR_stack.pop()

      key_node = self._node_stack.pop()
      if key_node['type'] == 'variable':
        rel_attr = RelationAttributePair(relation, keys[i])
        if key_node['node'].isFree():
          ir.setRelationAttributePairs([rel_attr])
        if not key_node['node'].bindTo(rel_attr):
          print 'Could not bind'
          print key_node['node'].getBoundValue()
          previous_binding = key_node['node'].getBoundValue()
          assert previous_binding != None
          prev_constraints = ir.getConstraintTree()
          new_constraint = Constraint(Constraint.EQ, rel_attr, \
            previous_binding)
          print 
          merged_constraint = None;
          if prev_constraints is None:
            ir.setConstraintTree(new_constraint)
          elif new_constraint is None:
            ir.setConstraintTree(prev_constraints)
          else:
            merged_constraint = AndConstraint(prev_constraints, new_constraint)
            ir.setConstraintTree(merged_constraint)

        merged_ir = self.conjunctIR(merged_ir, ir)
        key_values.append(key_node)

    self._IR_stack.append(merged_ir)

    state = {'type' : 'predicate',
             'table' : relation,
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
    rel_attr_pairs.extend(right_ir.getRelationAttributePairs())
    left_ir.setRelationAttributePairs(rel_attr_pairs)

    left_constraints = left_ir.getConstraintTree()
    right_constraints = right_ir.getConstraintTree()
    if left_constraints is None:
      left_ir.setConstraintTree(right_constraints)
    elif right_constraints is None:
      left_ir.setConstraintTree(left_constraints)
    else:
      left_constraints = AndConstraint(left_constraints, right_ir.getConstraintTree())
      left_ir.setConstraintTree(left_constraints)

    left_relation = left_ir.getRelationTree()
    right_relation = right_ir.getRelationTree()
    if left_relation is None:
      left_ir.setRelationTree(right_relation)
    elif right_relation is None or join_classifier == NO_JOIN:
      left_ir.setRelationTree(left_relation)
    else:
      if join_classifier == EQUI_JOIN:
        left_relation = EquiJoinNode(left_relation, right_ir.getRelationTree(), keys)
        left_ir.setRelationTree(left_relation)
      elif join_classifier == CROSS_JOIN:
        left_relation = CrossJoinNode(left_relation, right_ir.getRelationTree(), keys)
        left_ir.setRelationTree(left_relation)

    return left_ir

  def disjunctIR(self, left_ir, right_ir):
    rel_attr_pairs = left_ir.getRelationAttributePairs()
    rel_attr_pairs.extend(right_ir.getRelationAttributePairs())
    left_ir.setRelationAttributePairs(rel_attr_pairs)

    left_constraints = left_ir.getConstraintTree()
    right_constraints = right_ir.getConstraintTree()
    if left_constraints is None:
      left_ir.setConstraintTree(right_constraints)
    elif right_constraints is None:
      left_ir.setConstraintTree(left_constraints)
    else:
      left_constraints = OrConstraint(left_constraints, right_ir.getConstraintTree())
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
