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
    string = node.getRelation().getAlias() + "." + node.getAttribute()
    if self._expecting_constraint:
      self._expecting_constraint = False
      self._sql_where_stack.append(string)
    else:
      self._sql_select_list.append(string)

  @v.when(ir.StringLiteral)
  def visit(self, node):
    self._sql_where_stack.append("'" + node.getString() + "'")

  @v.when(ir.RelationNode)
  def visit(self, node):
    relation_alias = None
    if node.hasAlias():
      relation_alias = node.getName() + ' AS ' + node.getAlias()
    else:
      relation_alias = node.getName()
    self._sql_from_stack.append(relation_alias)

  @v.when(ir.CrossJoinNode)
  def visit(self, node):
    node.getLeft().accept(self)
    node.getRight().accept(self)
    rightString = self._sql_from_stack.pop()
    leftString = self._sql_from_stack.pop()
    joinString = leftString + " CROSS JOIN " + rightString
    self._sql_from_stack.append(joinString)

  @v.when(ir.EquiJoinNode)
  def visit(self, node):
    node.getLeft().accept(self)
    node.getRight().accept(self)
    rightString = self._sql_from_stack.pop()
    leftString = self._sql_from_stack.pop()
    node.getConstraintTree().accept(self)
    constraintString = self._sql_where_stack.pop()
    joinString = "(" + leftString + ") JOIN " + \
                 "(" + rightString + ") ON " + constraint_String
    self._sql_from_stack.append(joinString)

  @v.when(ir.Constraint)
  def visit(self, node):
    print node.getLeftTerm().getRelation().getAlias()
    print node.getLeftTerm().getAttribute()
    self._expecting_constraint = True
    node.getLeftTerm().accept(self)
    self._expecting_constraint = True
    node.getRightTerm().accept(self)
    rightString = self._sql_where_stack.pop()
    leftString = self._sql_where_stack.pop()
    opString = node.getOp()
    constraintString = leftString + " " + opString + " " + rightString
    self._sql_where_stack.append(constraintString)

  @v.when(ir.AndConstraint)
  def visit(self, node):
    node.getLeftConstraint().accept(self)
    node.getRightConstraint().accept(self)
    rightString = self._sql_where_stack.pop()
    leftString = self._sql_where_stack.pop()
    constraintString = "(" + leftString + ") AND " + \
                       "(" + rightString + ")"
    self._sql_where_stack.append(constraintString)

  @v.when(ir.OrConstraint)
  def visit(self, node):
    node.getLeftConstraint().accept(self)
    node.getRightConstraint().accept(self)
    rightString = self._sql_where_stack.pop()
    leftString = self._sql_where_stack.pop()
    constraintString = "(" + leftString + ") OR " + \
                       "(" + rightString + ")"
    self._sql_where_stack.append(constraintString)

  @v.when(ir.UnaryConstraint)
  def visit(self,node):
    print 'Generating code for unary constraint'
    node.getConstraint().accept(self)
    childString = self._sql_where_stack.pop()
    constraintString = node.getOp() + "(" + childString + ")"
    self._sql_where_stack.append(constraintString)


