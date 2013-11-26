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

    self._invert_dict = { '=' : invert_EQ,
                          '<>': invert_NEQ,
                          '>' : invert_LT,
                          '>=': invert_LTE,
                          '<' : invert_GT,
                          '<=': invert_GTE,
                          'IS': invert_IS,
                          'IS NOT' : invert_ISNOT,
                          'NULL': invert_NULL, }

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
    # Pop relevant objects off the stack
    right_node = self.popNode()
    left_node = self.popNode()
    right_ir = self.popIR()
    left_ir = self.popIR()

    # Sanity check the objects
    assert left_node
    assert right_node

    # Precompute some booleans to make cases easier to understand
    both_predicates = right_node['type'] == 'predicate' and \
                      left_node['type'] == 'predicate'
    mixture_constraints_predicates = (right_node['type'] == 'predicate' and \
                                      left_node['type'] == 'constraint') or \
                                     (right_node['type'] == 'constraint' and \
                                      left_node['type'] == 'predicate')

    # Check the left and right nodes are both predicates
    if both_predicates:
      right_keys = right_node['keys']
      left_keys = left_node['keys']
      right_keyvals = right_node['key_values']
      left_keyvals = left_node['key_values']
      right_table = right_node['table']
      left_table = left_node['table']

      # Determine if the tables are the same
      if right_table.getName() == left_table.getName():
        right_types = [x['type'] for x in right_keyvals]
        left_types = [x['type'] for x in left_keyvals]

        # Check if every element is a variable
        if all(x == 'variable' for x in left_types) \
          and all(x == 'variable' for x in right_types):
          right_ids = [x['node'].getIdentifier() for x in right_keyvals]
          left_ids = [x['node'].getIdentifier() for x in left_keyvals]
          # Finally check if each and every element is the same
          if right_ids == left_ids:
            # Should push the equal table on to the stack
            self.conjunctIR(left_ir, right_ir)
            self.pushIR(left_ir)
            state = {
                'type' : 'predicate',
                'table' : left_table,
                'key_values' : left_keyvals,
                'keys' : left_keys
              }
            self.pushNode(state)
            return

        # Tables are still equal, but elements are variables with different
        # identifiers, or are not all variables. Iterate through the keys,
        # working out where to join.

        # Alias the relations
        left_table.setAlias(left_table.getName() + '1')
        right_table.setAlias(right_table.getName() + '2')

        join_constraints = None

        # Loop through left and right keyvals
        for i in range(0, len(left_keyvals)):
          for j in range(0, len(right_keyvals)):
            left_key  = left_keyvals[i]
            right_key = right_keyvals[j]
            left_rel_attr  = RelationAttributePair(left_table, left_keys[i])
            right_rel_attr = RelationAttributePair(right_table, right_keys[j])
            left_key_node_id  = left_key['node'].getIdentifier()
            right_key_node_id = right_key['node'].getIdentifier()
            # Check if both keys are variables
            if left_key['type'] == right_key['type'] == 'variable':
              # If the identifiers match, add this as a constraint
              if left_key_node_id == right_key_node_id:
                constraint = Constraint(Constraint.EQ, \
                                        left_rel_attr, right_rel_attr)
                if join_constraints is None:
                  join_constraints = constraint
                else:
                  join_constraints = AndConstraint(join_constraints, constraint)
            else:
              print """a mixture of variables and constants found, add some
              constraints"""

        # Join constraints calculated. Now work out how to join.
        if join_constraints is None:
          self.conjunctIR(left_ir, right_ir, JoinTypes.CROSS_JOIN)
        else:
          self.conjunctIR(left_ir, right_ir, JoinTypes.Join, join_constraints)
        state = {'type' : 'join',
                'table' : left_ir.getRelationTree(),
                'key_values' : left_keyvals + right_keyvals
                }
        self.pushNode(state)
        self.pushIR(left_ir)
      else:
        print 'Tables are different'
    # Mixture of predicates and constraints
    elif mixture_constraints_predicates:
      print 'Mixture!'
      left_is_predicate = left_node['type'] == 'predicate'
      if left_is_predicate:
        print 'Left is predicate'
        self.conjunctIR(left_ir, right_ir)
        self.pushIR(left_ir)
        self.pushNode(left_node)
      else:
        print 'Right is predicate'
        self.conjunctIR(right_ir, left_ir)
        self.pushIR(right_ir)
        self.pushNode(right_node)
    else:
      print 'Both constraints'
      self.conjunctIR(left_ir, right_ir)
      self.pushIR(left_ir)
      self.pushNode(left_node)
    print "And(",left_node,",",right_node,")"

  @v.when(ast.NotNode)
  def visit(self, node):
    child = self.popNode()
    ir = self.popIR()
    ### CASE 1: ~Constraint
    #### Simply invert the constraint
    if child['type'] == 'constraint'
      print 'Evaluating negation of constraint'  
      op = ir.getOp()
      print 'Inverting: ' + op
      op = self._invert_dict[op]()
      print 'Inverted: ' + op
      left = ir.getLeftTerm()
      right = ir.getRightTerm()
      self.pushIR(Constraint(op,left,right))
      
      #Invert constraint

    ### Case 2: ~Predicate(x,y)
    #### Compute the set difference
    else if child['type'] == 'Predicate'

    ### Case 3: ~(A /\ B)
    #### I'm unsure about this case.
    #### Perhaps we can just push the not inside
    #### the brackets and forget about this case.
    else if child['type'] == 'AND node'

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
    relation = RelationNode(attributes[0])
    # Retrieve the primary keys from the schema
    keys = self._schema.getPrimaryKeys(relation.getName())
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
    print '#########',keys
    for i in reversed(range(0, len(keys))):
      attr = keys[i]
      child = self.popNode()
      ir = self.popIR()
      child_type = child['type']
      child_node = child['node']
      rel_attr = RelationAttributePair(relation, attr)
      # Check if a variable.
      if child_type == 'variable':
        # If a child is not quantified, add to the projection list
        if child_node.isFree():
          ir.setRelationAttributePairs([rel_attr])
        self.bind(child_node, rel_attr, ir)
        print 'Binding',child_node.getIdentifier(),'to',rel_attr.getAttribute()
        if i < key_count:
          key_values.append(child)
      elif child_type == 'string_lit':
        # Add a constraint that the attribute should equal the relevant value
        prev_constraints = ir.getConstraintTree()
        lit = StringLiteral(child_node.getValue())
        new_constraint = Constraint(Constraint.EQ, rel_attr, lit)
        if prev_constraints is None:
          ir.setConstraintTree(new_constraint)
        else:
          ir.setConstraintTree(AndConstraint(prev_constraints, new_constraint))
      else:
        print 'ConstantNode'
      # Lazy instantiation of merged_ir.
      if merged_ir is None:
        merged_ir = ir
      # Merging IRs
      else:
        merged_ir = self.conjunctIR(ir, merged_ir)

    # Add the relation from the predicate to the IR
    merged_ir.setRelationTree(relation)

    # Push the IR for the predicate node onto the IR stack.
    self.pushIR(merged_ir)

    # Push some other state onto the node stack for the combining entity to
    # consume.
    state = {
        'type': 'predicate',
        'table': relation,
        'key_values': key_values,
        'keys': keys
      }
    self.pushNode(state)
    print self._node_stack

  @v.when(ast.BinaryOperatorNode)
  def visit(self, node):
    # Set up state and operator
    op = node.getOp()
    op = self.binOpToConstraintsOp(op)
    state = {
        'type': 'constraint',
        'node': node
      }

    # Pop relevant objects off the stack
    right_child = self.popNode()
    left_child = self.popNode()
    right_ir = self.popIR()
    left_ir = self.popIR()

    # Precompute booleans for clearer conditions later
    both_variables = left_child['type'] == right_child['type'] == 'variable'
    right_variable_left_string_lit = \
      right_child['type'] == 'variable' and left_child['type'] == 'string_lit'
    left_variable_right_string_lit = \
      right_child['type'] == 'string_lit' and left_child['type'] == 'variable'
    mixture_variables_string_lits = \
      left_variable_right_string_lit or right_variable_left_string_lit

    # Pre-conjunct the left and right IRs for later use
    self.conjunctIR(left_ir, right_ir)
    prev_constraints = left_ir.getConstraintTree()

    if both_variables:
      print 'Both variables'
      # Bind two variables together
      bind(left_child['node'], right_child['node'], left_ir)

    elif mixture_variables_string_lits:
      if left_variable_right_string_lit:
        print 'Left variable, right string lit'
        var_node = left_child['node']
        lit_node = right_child['node']
      else:
        print 'Right variable, left string lit'
        var_node = right_child['node']
        lit_node = left_child['node']

      # Constrain the variable to the string literal
      constraint = Constraint(op, var_node.getBoundValue(), \
                              StringLiteral(lit_node.getValue()))
      # Add it to the IR
      if prev_constraints is None:
        left_ir.setConstraintTree(constraint)
      else:
        left_ir.setConstraintTree(AndConstraint(prev_constraints, constraint))

    # Finally, push relevant objects onto the stacks
    self.pushIR(left_ir)
    self.pushNode(state)
    print "Seen BinaryOperatorNode"

  def binOpToConstraintsOp(self, op):
    return {
        ast.BinaryOperatorNode.EQ : Constraint.EQ,
        ast.BinaryOperatorNode.LT : Constraint.LT,
        ast.BinaryOperatorNode.LTE : Constraint.LTE,
        ast.BinaryOperatorNode.GT : Constraint.GT,
        ast.BinaryOperatorNode.GTE : Constraint.GTE,
        ast.BinaryOperatorNode.NEQ : Constraint.NEQ
    }[op]

  @v.when(ast.FunctionNode)
  def visit(self, node):
    print "Seen FunctionNode"

  # TODO Refactor replicated code here...
  @v.when(ast.StringLitNode)
  def visit(self, node):
    ir = IR()
    state = {'type' : 'string_lit', 'node' : node}
    self.pushNode(state)
    self.pushIR(ir)

  # TODO ...and here...
  @v.when(ast.ConstantNode)
  def visit(self, node):
    ir = IR()
    state = {'type' : 'constant', 'node' : node}
    self.pushNode(state)
    self.pushIR(ir)
    print "Seen ConstantNode"

  # TODO ...and here.
  @v.when(ast.VariableNode)
  def visit(self, node):
    ir = IR()
    state = {'type' : 'variable', 'node' : node}
    self.pushNode(state)
    self.pushIR(ir)
    print "Seen VariableNode"

# Stack manipulating functions

  def pushNode(self, node):
    self._node_stack.append(node)

  def popNode(self):
    return self._node_stack.pop()

  def pushIR(self, ir):
    self._IR_stack.append(ir)

  def popIR(self):
    return self._IR_stack.pop()

# Bindings

  def bind(self, node, rel_attr, ir):
    if not node.bindTo(rel_attr):
      # Get the previous binding
      previous_binding = node.getBoundValue()
      assert previous_binding is not None
      # Add to the constraints
      prev_constraints = ir.getConstraintTree()
      print '#####',rel_attr.getAttribute(),"=",previous_binding.getAttribute(),node.getIdentifier()
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

  def combineRelations(self, left_ir, right_ir, join_type, keys=None):
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
        left_relation = CrossJoinNode(left_relation, right_ir.getRelationTree())
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

  def conjunctIR(self, left_ir, right_ir, join_classifier=JoinTypes.NO_JOIN,
      keys=None):
    self.extendRelationAttributePairs(left_ir, right_ir)
    self.combineConstraints(left_ir, right_ir, ConstraintBinOp.AND)
    self.combineRelations(left_ir, right_ir, join_classifier, keys)

    return left_ir

  def disjunctIR(self, left_ir, right_ir):
    self.extendRelationAttributePairs(left_ir, right_ir)
    self.combineConstraints(left_ir, right_ir, ConstraintBinOp.OR)
    self.combineRelations(left_ir, right_ir, JoinTypes.NO_JOIN)

    return left_ir

  def getIR(self):
    return self._IR_stack[0]


##functions used to invert constraint ops
  def invert_EQ(self):
    return '<>'
  
  def invert_NEQ(self):
    return '='
  
  def invert_GT(self):
    return '<='

  def invert_GTE(self):
    return '<'

  def invert_LT(self):
    return '>='

  def invert_LTE(self):
    return '>'

  def invert_IS(self):
    return 'IS NOT'

  def invert_ISNOT(self):
    return 'IS'

  def invert_NULL(self):
    return 'NOT NULL'
