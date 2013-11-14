'''
Generic Logic AST Visitor
This class implements the visitor pattern over the AST, converting it to a
generic intermediate representation for code generation.
'''

import visit as v
import ast
from codegen.ir import *
from copy import copy, deepcopy

class GenericLogicASTVisitor():

  def __init__(self, schema):
    # Instance variables go here, if necessary
    self._node_stack = []
    self._IR_stack = []
    self._schema = schema

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
    right_keys = right_node['keys']
    left_keys = left_node['keys']
    right_keyvals = right_node['key_values']
    left_keyvals = left_node['key_values']
    right_table = right_node['table']
    left_table = left_node['table']
    # Check the left and right nodes are both predicates
    if right_node['type'] == left_node['type'] == 'predicate':
      # Determine if the tables are the same
      if right_table == left_table:
        right_types = [x['type'] for x in right_keyvals]
        left_types = [x['type'] for x in left_keyvals]
        # Check if every element is a variable
        if all(x == 'variable' for x in left_types) \
            and all(x == 'variable' for x in right_types):
          right_ids = [x['node'].getIdentifier() for x in right_keyvals]
          left_ids = [x['node'].getIdentifier() for x in left_keyvals]
          # Finally check if each and every element is the same!
          if right_ids == left_ids:
            # Should push the equal table on to the stack
            ir = self.conjunctIR(left_ir, right_ir)
            self._IR_stack.append(ir)
            self._node_stack.append(left_table)
            return
        # Tables are still equal, but elements are not all variables, iterate
        # pairwise through the list.
        constraints_list = []
        for i in range(0, len(right_keyvals)): # TODO: arbitrary - refactor
          left_key = left_keyvals[i]
          right_key = right_keyvals[i]
          if right_key['type'] == left_key['type'] == 'variable':
            if right_key['node'].getIdentifier() == left_key['node'].getIdentifier():
              # Need to add this to the constraint list
              left_rel_attr = RelationAttributePair(left_table, left_key['node'])
              right_rel_attr = RelationAttributePair(right_table, right_key['node'])
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
    keys = self._schema.getPrimaryKeys(relation)
    # Sort the keys alphabetically as our predicates enforce this
    keys = sorted(keys)
    # Iterate over the children from right to left, matching binding values
    # Python syntax: [1:] ignores first value (index 0), so 1 to end of list.
    binding_values = attributes[1:]
    merged_ir = None

    key_count = len(keys)
    key_values = []

    # Reverse iterate over the parameters, matching them with keys or
    # attributes as necessary, binding them and passing keys up to any consumer
    # node i.e and AndNode.
    keys.extend(binding_values)
    for i in reversed(range(0, len(keys))):
      attr = keys[i]
      child = self._node_stack.pop()
      ir = self._IR_stack.pop()
      child_type = child['type']
      child_node = child['node']
      rel_attr = RelationAttributePair(relation, attr)
      # Check if a variable.
      if child_type == 'variable':
        # If a child is not quantified, add to the projection list
        if child_node.isFree():
          ir.setRelationAttributePairs([rel_attr])
        self.bind(child_node, rel_attr, ir)
        if i < key_count:
          key_values.append(child)
      elif child_type == 'string_lit':
        prev_constraints = ir.getConstraintTree()
        lit = StringLiteral(child_node.getValue())
        print lit, ",", child_node.getValue()
        new_constraint = Constraint(Constraint.EQ, rel_attr, lit)
        if prev_constraints is None:
          ir.setConstraintTree(new_constraint)
        else:
          ir.setConstraintTree(AndConstraint(prev_constraints, new_constraint))
      else:
        print 'ConstantNode'
      if merged_ir is None:
        merged_ir = ir
      else:
        merged_ir = self.conjunctIR(merged_ir, ir)

    merged_ir.setRelationTree(RelationNode(relation))

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

  @v.when(ast.StringLitNode)
  def visit(self, node):
    state = {'type' : 'string_lit', 'node' : node}
    self._node_stack.append(state)
    ir = IR()
    self._IR_stack.append(ir)

  @v.when(ast.ConstantNode)
  def visit(self, node):
    state = {'type' : 'constant', 'node' : node}
    self._node_stack.append(state)
    ir = IR()
    self._IR_stack.append(ir)
    print "Seen ConstantNode"

  @v.when(ast.VariableNode)
  def visit(self, node):
    ir = IR()
    state = {'type' : 'variable', 'node' : node}
    self._node_stack.append(state)
    self._IR_stack.append(ir)
    print "Seen VariableNode"

# Bindings

  def bind(self, node, rel_attr, ir):
    if not node.bindTo(rel_attr):
      # Get the previous binding
      previous_binding = node.getBoundValue()
      assert previous_binding != None
      # Add to the constraints
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

# Combining IRs

  def extendRelationAttributePairs(self, left_ir, right_ir):
    """
    Concatenates together two sets of relation attribute pairs, updating the
    left IR. This is primarily used when merging together IRs
    """
    rel_attr_pairs = left_ir.getRelationAttributePairs()
    rel_attr_pairs.extend(right_ir.getRelationAttributePairs())
    left_ir.setRelationAttributePairs(rel_attr_pairs)

  def combineRelations(self, left_ir, right_ir, join_type):
    """
    Combines two Relation trees, leaving the result in the left_irs
    relationTree attribute. This is primarily used when merging together two
    IRs. Possible values for join_type is defined in the JoinTypes class within
    codegen.ir.
    """
    left_relation = left_ir.getRelationTree()
    right_relation = right_ir.getRelationTree()
    if left_relation is None:
      left_ir.setRelationTree(right_relation)
    elif right_relation is None or join_type == JoinTypes.NO_JOIN:
      left_ir.setRelationTree(left_relation)
    else:
      if join_type == JoinTypes.EQUI_JOIN:
        left_relation = EquiJoinNode(left_relation, right_ir.getRelationTree(), keys)
        left_ir.setRelationTree(left_relation)
      elif join_type == JoinTypes.CROSS_JOIN:
        left_relation = CrossJoinNode(left_relation, right_ir.getRelationTree(), keys)
        left_ir.setRelationTree(left_relation)

  def combineConstraints(self, left_ir, right_ir, bin_op):
    """
    Combines two sets of constraints from seperate IRs, leaving the result in
    the left IR. This is primarily used when merging together IRs. The bin_op
    passed in should be a flag as defined in the ConstraintBinOp class.
    """
    left_constraints = left_ir.getConstraintTree()
    right_constraints = right_ir.getConstraintTree()
    if left_constraints is None:
      left_ir.setConstraintTree(right_constraints)
    elif right_constraints is None:
      left_ir.setConstraintTree(left_constraints)
    else:
      if bin_op == ConstraintBinOp.AND:
        left_constraints = AndConstraint(left_constraints, right_ir.getConstraintTree())
      elif bin_op == ConstraintBinOp.OR:
        left_constraints = OrConstraint(left_constraints, right_ir.getConstraintTree())
      left_ir.setConstraintTree(left_constraints)

  def conjunctIR(self, left_ir, right_ir, join_classifier=JoinTypes.NO_JOIN, keys=[]):
    self.extendRelationAttributePairs(left_ir, right_ir)
    self.combineConstraints(left_ir, right_ir, ConstraintBinOp.AND)
    self.combineRelations(left_ir, right_ir, join_classifier)

    return left_ir

  def disjunctIR(self, left_ir, right_ir):
    self.extendRelationAttributePairs(left_ir, right_ir)
    self.combineConstraints(left_ir, right_ir, ConstraintBinOp.OR)
    self.combineRelations(left_ir, right_ir, JoinTypes.NO_JOIN)

    return left_ir
