'''
SQL Generator
This class takes the SQL intermediate representation and converts it into an
SQL query string ready for a DBMS to interpret.
'''

import visit as v
import ir

class SQLGenerator():

  def __init__(self):
    self._sql = ""
    self._expecting_constraint = False
    self._sql_select_list = []
    self._sql_from_stack = []
    self._sql_where_stack = []

  def getSQL(self):
    return self._sql

  @v.on('node')
  def visit(self, node):
    # Generic node, don't think you're supposed to change this
    pass

  @v.when(ir.IR)
  def visit(self, node):
    self._sql += "SELECT "
    self._sql += ", ".join(self._sql_select_list)
    self._sql += " FROM "
    self._sql += self._sql_from_stack[0]
    if len(self._sql_where_stack) > 0:
      self._sql += " WHERE "
      self._sql += self._sql_where_stack[0]

  @v.when(ir.RelationAttributePair)
  def visit(self, node):
    print '*** SQL Generator: Begin RelationAttributePair ***'

    string = node.getRelation().getAlias() + "." + node.getAttribute()
    if self._expecting_constraint:
      self._expecting_constraint = False
      self._sql_where_stack.append(string)
    else:
      self._sql_select_list.append(string)
    print '*** SQL Generator: End RelationAttributePair ***'
  @v.when(ir.VariableNode)
  def visit(self, node):
    print '*** SQL Generator: Begin VariableNode ***'
    self._sql_where_stack.append(node.getIdentifier())
    print '*** SQL Generator: End VariableNode ***'

  @v.when(ir.StringLiteral)
  def visit(self, node):
    print '*** SQL Generator: Begin StringLiteral ***'
    self._sql_where_stack.append("'" + node.getString() + "'")
    print '*** SQL Generator: End StringLiteral ***'

  @v.when(ir.RelationNode)
  def visit(self, node):
    print '*** SQL Generator: Begin RelationNode ***'
    relation_alias = None
    if node.hasAlias():
      relation_alias = node.getName() + ' AS ' + node.getAlias()
    else:
      relation_alias = node.getName()
    self._sql_from_stack.append(relation_alias)
    print '*** SQL Generator: End RelationNode ***'

  @v.when(ir.CrossJoinNode)
  def visit(self, node):
    print '*** SQL Generator: Begin CrossJoinNode ***'
    node.getLeft().accept(self)
    node.getRight().accept(self)
    rightString = self._sql_from_stack.pop()
    leftString = self._sql_from_stack.pop()
    joinString = leftString + " CROSS JOIN " + rightString
    self._sql_from_stack.append(joinString)
    print '*** SQL Generator: End CrossJoinNode ***'

  @v.when(ir.EquiJoinNode)
  def visit(self, node):
    print '*** SQL Generator: Begin EquiJoinNode ***'
    node.getLeft().accept(self)
    node.getRight().accept(self)
    rightString = self._sql_from_stack.pop()
    leftString = self._sql_from_stack.pop()
    node.getConstraintTree().accept(self)
    constraintString = self._sql_where_stack.pop()
    joinString = leftString + " JOIN " + \
                 rightString + " ON " + constraintString
    self._sql_from_stack.append(joinString)
    print '*** SQL Generator: End EquiJoinNode ***'

  @v.when(ir.Constraint)
  def visit(self, node):
    print '*** SQL Generator: Begin Constraint ***'
    print node.getLeftTerm().getRelation().getAlias()
    print node.getLeftTerm().getAttribute()
    print str(node.getRightTerm())

    self._expecting_constraint = True
    node.getLeftTerm().accept(self)
    self._expecting_constraint = True
    node.getRightTerm().accept(self)
    print self._sql_where_stack
    rightString = self._sql_where_stack.pop()
    if self._sql_where_stack:
      leftString = self._sql_where_stack.pop()
    else: 
      leftString = ''
    opString = node.getOp()
    if leftString == 'IS NULL':
      constraintString = rightString + " " + leftString
    else:
      constraintString = leftString + " " + opString + " " + rightString
    print '\tConstraint Added: ' + constraintString
    self._sql_where_stack.append(constraintString)
    print '*** SQL Generator: End Constraint ***'

  @v.when(ir.AndConstraint)
  def visit(self, node):
    print '*** SQL Generator: Begin AndConstraint ***'
    node.getLeftConstraint().accept(self)
    node.getRightConstraint().accept(self)
    rightString = self._sql_where_stack.pop()
    leftString = self._sql_where_stack.pop()
    constraintString = "(" + leftString + ") AND " + \
                       "(" + rightString + ")"
    self._sql_where_stack.append(constraintString)
    print '*** SQL Generator: End AndConstraint ***'
  
  @v.when(ir.OrConstraint)
  def visit(self, node):
    print '*** SQL Generator: Begin OrConstraint ***'
    node.getLeftConstraint().accept(self)
    node.getRightConstraint().accept(self)
    rightString = self._sql_where_stack.pop()
    leftString = self._sql_where_stack.pop()
    constraintString = "(" + leftString + ") OR " + \
                       "(" + rightString + ")"
    self._sql_where_stack.append(constraintString)
    print '*** SQL Generator: End OrConstraint ***'

  @v.when(ir.UnaryConstraint)
  def visit(self,node):
    print '*** SQL Generator: Begin UnaryConstraint ***'
    constraints = node.getConstraint()
    if constraints is not None:
      constraints.accept(self)
      childString = self._sql_where_stack.pop()
      constraintString = node.getOp() + ' ' + childString + ' '
      print '\tUnary Constraint Added: ' + constraintString
      self._sql_where_stack.append(constraintString)
    else:
      print 'Unfortunately there were no constraints my good chap.\nCarry on!'
    print '*** SQL Generator: End UnaryConstraint ***'

  @v.when(ir.NullNode)
  def visit(self,node):
    print '*** SQL Generator: Begin NullNode ***'
    constraintString = "IS NULL"
    self._sql_where_stack.append(constraintString)
    print '*** SQL Generator: End NullNode ***'
  
