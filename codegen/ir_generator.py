'''
IR Generator
This class implements the visitor pattern over the AST, converting it to an
intermediate representation for further code generation.
'''

import visit as v
import ast
from codegen.ir import *

from copy import copy, deepcopy

class IRGenerator:

  def __init__(self, schema):
    # Instance variables go here, if necessary
    self._node_stack = []
    self._IR_stack = []
    self._schema = schema
    self._alias = 1

  @v.on('node')
  def visit(self, node):
    # Generic node, don't think you're supposed to change this
    pass

  @v.when(ast.IffNode)
  def visit(self, node):
    print "*** IR Generator:  Begin IffNode - ERROR ***"
    print "*** IR Generator:  End IffNode - ERROR ***"

  @v.when(ast.OrNode)
  def visit(self, node):
    print "*** IR Generator:  Begin OrNode - ERROR ***"
    print "*** IR Generator:  End OrNode - ERROR ***"

  @v.when(ast.AndNode)
  def visit(self, node):
    print "*** IR Generator:  Begin AndNode ***"
    # Pop relevant objects off the stack
    right_node = self.popNode()
    left_node = self.popNode()
    right_ir = self.popIR()
    left_ir = self.popIR()
    print '\tLeft IR: ' + str(left_ir)
    print '\tRight IR: ' + str(right_ir)

    # Sanity check the objects
    assert left_node
    assert right_node

    # Precompute some booleans to make cases easier to understand
    both_predicates = right_node['type'] == 'predicate' and \
                      left_node['type'] == 'predicate'
    both_constraints = right_node['type'] == 'constraint' and \
                      left_node['type'] == 'constraint'
    mixture_constraints = left_node['type'] == 'constraint' or \
                      right_node['type'] == 'constraint'
    mixture_exists = left_node['type'] == 'thereexists' or \
                      right_node['type'] == 'thereexists'
    mixture_forall = left_node['type'] == 'forall' or \
                      right_node['type'] == 'forall'

    # Check the left and right nodes are both predicates
    if both_predicates:
      right_keys = right_node['keys']
      left_keys = left_node['keys']
      right_keyvals = right_node['key_values']
      left_keyvals = left_node['key_values']
      left_attr_vals = left_node['attr_values']
      right_attr_vals = right_node['attr_values']
      left_attrs = left_node['attrs']
      right_attrs = right_node['attrs']

      left_comb_vals = left_keyvals + left_attr_vals
      right_comb_vals = right_keyvals + right_attr_vals
      left_comb_keys = left_keys + left_attrs
      right_comb_keys = right_keys + right_attrs

      left_tables = set([x.getRelation() for x in left_keys])
      right_tables = set([x.getRelation() for x in right_keys])
      left_tables_alias = set([x.getAlias() for x in left_tables])
      right_tables_alias = set([x.getAlias() for x in right_tables])

      # Determine if the tables are the same
      table_intersections = left_tables_alias.intersection(right_tables_alias)
      for matching_table in table_intersections:

        filtered_left_keyvals = []
        filtered_right_keyvals = []

        for i in range(0, len(left_keyvals)):
          if left_keys[i].getRelation().getAlias() == matching_table:
            filtered_left_keyvals.append(left_keyvals[i])

        for i in range(0, len(right_keyvals)):
          if right_keys[i].getRelation().getAlias() == matching_table:
            filtered_right_keyvals.append(right_keyvals[i])

        left_types = [x['type'] for x in filtered_left_keyvals]
        right_types = [x['type'] for x in filtered_right_keyvals]

        # Check if every element is a variable
        if all(x == 'variable' for x in left_types) \
          and all(x == 'variable' for x in right_types):
          right_ids = [x['node'].getIdentifier() for x in filtered_right_keyvals]
          left_ids = [x['node'].getIdentifier() for x in filtered_left_keyvals]
          # Finally check if each and every element is the same
          if right_ids == left_ids:
            # Should push the equal table on to the stack
            self.conjunctIR(left_ir, right_ir)
            self.pushIR(left_ir)
            state = {
                'type' : 'predicate',
                'key_values' : left_keyvals + right_keyvals,
                'keys' : left_keys + right_keys,
                'attrs' : left_attrs + right_attrs,
                'attr_values' : left_attr_vals + right_attr_vals
              }
            self.pushNode(state)
            print 'Generated IR : ' + str(left_ir)
 #     print "\tAnd(",left_node,",",right_node,")"
            print "*** IR Generator:  End AndNode ***"

            return

      # Tables may be equal, but elements are variables with different
      # identifiers, or are not all variables. Iterate through the keys,
      # working out where to join.

      # Alias the relations. If there is only one alias in a given side of the
      # and node, it is not a join and so will need to be aliased. Otherwise, a
      # join has already occured, and so there is no need for a further alias.

      if len(left_tables) == 1:
        relation = iter(left_tables).next()
        if (relation.getAlias() in right_tables_alias):
          relation.setAlias(relation.getName() + self.getGlobalAliasNumber())
      if len(right_tables) == 1:
        relation = iter(right_tables).next()
        if (relation.getAlias() in left_tables_alias):
          relation.setAlias(relation.getName() + self.getGlobalAliasNumber())

      join_constraints = self.getJoinConstraints(left_comb_vals,
          right_comb_vals, left_comb_keys, right_comb_keys);

      # Join constraints calculated. Now work out how to join.
      if join_constraints is None:
        self.conjunctIR(left_ir, right_ir, JoinTypes.CROSS_JOIN)
      else:
        self.conjunctIR(left_ir, right_ir, JoinTypes.EQUI_JOIN,
            join_constraints)
        self.removeDuplicateConstraints(left_ir, join_constraints)
      state = {'type' : 'predicate',
               'keys' : left_keys + right_keys,
              'key_values' : left_keyvals + right_keyvals,
              'attrs' : left_attrs + right_attrs,
              'attr_values' : left_attr_vals + right_attr_vals
              }
      self.pushNode(state)
      self.pushIR(left_ir)
    # Mixture of predicates and constraints
    elif both_constraints:
      self.conjunctIR(left_ir, right_ir)
      self.pushIR(left_ir)
      self.pushNode(left_node)
    elif mixture_constraints:
      left_is_predicate = left_node['type'] == 'predicate'
      if left_is_predicate:
        self.conjunctIR(left_ir, right_ir)
        self.pushIR(left_ir)
        self.pushNode(left_node)
      else:
        self.conjunctIR(right_ir, left_ir)
        self.pushIR(right_ir)
        self.pushNode(right_node)
    elif mixture_exists:
      if (left_node['type'] == 'exists'):
        new_constraint = ExistsConstraint(left_ir)
        prev_constraints = right_ir.getConstraintTree()
        if (prev_constraints is None):
          right_ir.setConstraintTree(new_constraint)
        else:
          right_ir.setConstraintTree(AndConstraint(new_constraint,
            prev_constraints))
          right_ir.addRelationAttributePairs(left_ir.getRelationAttributePairs)
        self.pushIR(right_ir)
        self.pushNode(right_node)
      else:
        new_constraint = ExistsConstraint(right_ir)
        prev_constraints = left_ir.getConstraintTree()
        if (prev_constraints is None):
          left_ir.setConstraintTree(new_constraint)
        else:
          left_ir.setConstraintTree(AndConstraint(new_constraint,
            prev_constraints))
          left_ir.addRelationAttributePairs(right_ir.getRelationAttributePairs)
        self.pushIR(left_ir)
        self.pushNode(left_node)
    elif mixture_forall:
      pass
    print right_ir
    
 #     print "\tAnd(",left_node,",",right_node,")"
    print "*** IR Generator:  End AndNode ***"

  @v.when(ast.NotNode)
  def visit(self, node):
    child = self.popNode()
    ir = self.popIR()
    child_node = child['node']
    constraint_tree = ir.getConstraintTree()

    print '*** IR Generator: Begin NotNode ***'    
    print '\tCurrent IR: ' + ir.__repr__()
    ### CASE 1: ~Constraint
    #### Simply insert a NOT node into the constraint tree
    if child['type'] == 'constraint':
      print '\tEvaluating NOT(Constraint)' 
     
      ## Quick and dirty hack
      ## NOT(rest_of_tree) -> (rest_of_tree)
      if isinstance(constraint_tree,UnaryConstraint):
        print '\tRemoving redundant NOT'
        ir.setConstraintTree(constraint_tree.getConstraint())
      else:
        print '\tAdding NOT(constraints) to tree'
        ir.setConstraintTree(UnaryConstraint(Constraint.NOT,constraint_tree))
  

    ### Case 2: ~Predicate(x,y)
    #### Compute the set difference
    elif child['type'] == 'predicate':
      print '\tEvaluating Predicate Negation'
      # Case 2a: something of the form ~\Ez(foo_bar(x,z)) 
      # in which case we need to add the constraint that x has no bar
      if constraint_tree == None:
        print '\tSet constraint that z IS NULL'
        self.bind(child_node.getChildren()[1],NullNode(),ir)
        print '\tZ Now bound'
      # Case 2b: string literal -  ~foo_bar(x,'stringlit')
      else:
        print '\tCurrent constraint tree: ' 
        ir.setConstraintTree(UnaryConstraint(Constraint.NOT,constraint_tree))   
      
    self.pushIR(ir)
    state = {
       'type' : 'constraint',
       'notNode' : 'true',
       'node' : node 
    }
    self.pushNode(state)
    print '\tIR Generated: ' + str(ir)
    print '*** IR Generator: End NotNode ***'    

  @v.when(ast.ForAllNode)
  def visit(self, node):
    print ' *** IR Generator: Begin ForAllNode - Partially Implemented ***'    
    state = {
      'type' : 'forall'
    }
    self.pushNode(state)
    print ' *** IR Generator: End ForAllNode - Partially Implemented ***'    

  @v.when(ast.ThereExistsNode)
  def visit(self, node):
    print '*** IR Generator: Begin ThereExistsNode - Partially Implemented ***'    
    state = {
      'type' : 'thereexists'
    }
    self.pushNode(state)
    print '*** IR Generator: End ThereExistsNode - Partially Implemented ***'    
  @v.when(ast.PredicateNode)
  def visit(self, node):
    print '*** IR Generator: Begin PredicateNode ***'    
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
    elements = keys[:]
    elements.extend(binding_values)
    #keys.extend(binding_values)
    #print '\t#########',keys
    for i in reversed(range(0, len(elements))):
      attr = elements[i]
      child = self.popNode()
      ir = self.popIR()
      child_type = child['type']
      child_node = child['node']
      rel_attr = RelationAttributePair(relation, attr)
      if i < key_count:
        child['key'] = True
      elements[i] = rel_attr
      key_values.insert(0, child)
      # Check if a variable.
      if child_type == 'variable':
        # If a child is not quantified, add to the projection list
        if child_node.isFree():
          ir.addRelationAttributePair(rel_attr)
        self.bind(child_node, rel_attr, ir)
        print '\tBinding',child_node.getIdentifier(),'to',rel_attr.getAttribute()
        #if (i < key_count):
        #  key_values.append(child)
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
        print '\tConstantNode'
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
        'key_values': key_values[:key_count],
        'keys': elements[:key_count],
        'attr_values': key_values[key_count:],
        'attrs': elements[key_count:],
        'node' : node
      }
    self.pushNode(state)
    print '\t' + str(merged_ir)
    print '*** IR Generator: End PredicateNode ***'

  @v.when(ast.BinaryOperatorNode)
  def visit(self, node):
    print '*** IR Generator: Begin BinaryOperatorNode - Partially Implemented ***'
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
    one_variable_one_not = \
      left_child['type'] == 'variable' and right_child['type'] != 'variable' or\
      right_child['type'] == 'variable' and left_child['type'] != 'variable'

    # Pre-conjunct the left and right IRs for later use
    self.conjunctIR(left_ir, right_ir)
    prev_constraints = left_ir.getConstraintTree()

    if both_variables:
      print '\tBoth variables in == relationship -> binding'
      new_constraint = Constraint(op,
          left_child['node'].getBoundValue(),
          right_child['node'].getBoundValue())
      if (prev_constraints is None):
        left_ir.setConstraintTree(new_constraint)
      else:
        left_ir.setConstraintTree(AndConstraint(new_constraint,
          prev_constraints))

    elif one_variable_one_not or (both_variables and op != Constraint.EQ):
      var_child = self.getVariableNode(left_child, right_child)
      other_child = right_child if var_child == left_child else left_child

      constraint_var = var_child['node'].getBoundValue()
      if other_child['type'] == 'variable':
        constraint_other = VariableNode(other_child['node'].getIdentifier())
      elif other_child['type'] == 'string_lit':
        constraint_other = StringLiteral(other_child['node'].getValue())
      elif other_child['type'] == 'constant':
        constraint_other = Constant(other_child['node'].getValue())

      print '\tAdding constraint'
      if var_child == left_child:
        constraint = Constraint(op, constraint_var, constraint_other)
      else:
        constraint = Constraint(op, constraint_other, constraint_var)

      # Add it to the IR
      if prev_constraints is None:
        left_ir.setConstraintTree(constraint)
      else:
        left_ir.setConstraintTree(AndConstraint(prev_constraints, constraint))

    # TODO handle case of neither child being a variable node - reduce to T/F?
    else:
      pass

    # Finally, push relevant objects onto the stacks
    self.pushIR(left_ir)
    self.pushNode(state)
    print '*** IR Generator: End BinaryOperatorNode - Partially Implemented ***'

  def binOpToConstraintsOp(self, op):
    return {
        ast.BinaryOperatorNode.EQ : Constraint.EQ,
        ast.BinaryOperatorNode.LT : Constraint.LT,
        ast.BinaryOperatorNode.LTE : Constraint.LTE,
        ast.BinaryOperatorNode.GT : Constraint.GT,
        ast.BinaryOperatorNode.GTE : Constraint.GTE,
        ast.BinaryOperatorNode.NEQ : Constraint.NEQ
    }[op]

  # Returns the node which is of type 'variable'
  # If both are of type 'variable' then the first parameter is returned
  def getVariableNode(self, left, right):
    if left['type'] == 'variable':
      return left
    else:
      return right

  @v.when(ast.BooleanNode)
  def visit(self, node):
    # TODO Should be the same as the below nodes
    print ' *** IR Generator: Begin BooleanNode - Unimplemented ***'   
    print ' *** IR Generator: End BooleanNode - Unimplemented ***'     

  # TODO Refactor replicated code here...
  @v.when(ast.StringLitNode)
  def visit(self, node):
    print '*** IR Generator: Begin StringLitNode ***'   
    ir = IR()
    state = {'type' : 'string_lit', 'node' : node}
    self.pushNode(state)
    self.pushIR(ir)
    print '*** IR Generator: End StringLitNode ***'   

  # TODO ...and here...
  @v.when(ast.ConstantNode)
  def visit(self, node):
    print ' *** IR Generator: Begin ConstantNode ***'   

    ir = IR()
    state = {'type' : 'constant', 'node' : node}
    self.pushNode(state)
    self.pushIR(ir)
    print ' *** IR Generator: End ConstantNode ***'   
  # TODO ...and here.
  @v.when(ast.VariableNode)
  def visit(self, node):
    print '*** IR Generator: Begin VariableNode ***'   
    ir = IR()
    state = {'type' : 'variable', 'node' : node}
    self.pushNode(state)
    print "\tSeen Variable: " + str(node.getIdentifier())
    self.pushIR(ir)
    print '*** IR Generator: End VariableNode ***'   


# Stack manipulating functions

  def pushNode(self, node):
    self._node_stack.append(node)

  def popNode(self):
    return self._node_stack.pop()

  def pushIR(self, ir):
    self._IR_stack.append(ir)

  def popIR(self):
    return self._IR_stack.pop()

# Solve join constraints

  def getGlobalAliasNumber(self):
    result = self._alias
    self._alias = self._alias + 1
    return str(result)

  # Loop through left and right keyvals
  def getJoinConstraints(self, left_keyvals, right_keyvals, left_keys,
      right_keys):
    join_constraints = None
    for i in range(0, len(left_keyvals)):
      for j in range(0, len(right_keyvals)):
        left_key_val  = left_keyvals[i]
        right_key_val = right_keyvals[j]
        left_rel_attr  = left_keys[i]
        right_rel_attr = right_keys[j]
        # Check if both keys are variables
        if left_key_val['type'] == right_key_val['type'] == 'variable':
          left_key_node_id  = left_key_val['node'].getIdentifier()
          right_key_node_id = right_key_val['node'].getIdentifier()
          # If the identifiers match, add this as a constraint
          if left_key_node_id == right_key_node_id:
            constraint = Constraint(Constraint.EQ, \
                                    left_rel_attr, right_rel_attr)
            if join_constraints is None:
              join_constraints = constraint
            else:
              join_constraints = AndConstraint(join_constraints, constraint)
        else:
          print """\ta mixture of variables and constants found, add some
          constraints"""
    print '\t\t\tJoin constraints: ' + str(join_constraints)
    return join_constraints

# Bindings

  def bind(self, node, rel_attr, ir):
    if not node.bindTo(rel_attr):
      # Get the previous binding
      previous_binding = node.getBoundValue()
      assert previous_binding is not None
      # Add to the constraints
      prev_constraints = ir.getConstraintTree()
      print '\t#####',rel_attr.getAttribute(),"=",previous_binding.getAttribute(),node.getIdentifier()
      new_constraint = Constraint(Constraint.EQ, rel_attr, previous_binding)
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
    left_ir.addRelationAttributePairs(right_ir.getRelationAttributePairs())

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

  def removeDuplicateConstraints(self, ir, constraints):
    ir_constraints = ir.getConstraintTree()
    ir.setConstraintTree(self.constraintTreeWithoutDuplicates(ir_constraints,
      constraints))

  def constraintTreeWithoutDuplicates(self, c1, c2):
    if (c1 == c2):
      return None
    if (isinstance(c1, ConstraintBinOp)):
      left = self.constraintTreeWithoutDuplicates(c1._left,
        c2)
      right = self.constraintTreeWithoutDuplicates(c1._right, c2)
      if (ir._left is None):
        return ir._right
      elif (ir._right is None):
        return ir._left
      c1._left = left
      c1._right = right
    return c1

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

