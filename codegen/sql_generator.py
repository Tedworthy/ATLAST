'''
SQL Generator
This class takes the SQL intermediate representation and converts it into an
SQL query string ready for a DBMS to interpret.
'''

import visit as v
import sqlir
import ast
import table_structure

class SQLGenerator():

  def __init__(self):
    self._sql = ""
    self._sql_select_list = []
    self._sql_join_stack = []
    self._sql_constraint_list = []

  @v.on('node')
  def visit(self, node):
    # Generic node, don't think you're supposed to change this
    pass

  @v.when(sqlir.SQLIR)
  def visit(self, node):
    self._sql += "SELECT "
    self._sql += ",".join(self._sql_select_list)
    self._sql += " FROM "
    self._sql += self._sql_join_stack[0]
    self._sql += " WHERE "
    #self._sql += _sql_constraint_list ##### WHY A CONSTRAINT STACK NOT A TREE?

  @v.when(ast.VariableNode)
  def visit(self, node):
    self._sql_select_list.append(node.getIdentifier())
    print "SQL Gen sees VariableNode"

  @v.when(table_structure.Table)
  def visit(self, node):
    # Unfinished data structures here.
    # We basically want to call accept on the child nodes (if a join node or
    # similar) and then convert to SQL string, popping the children off the
    # stack if necessary, and then pushing the result to the stack. Or if we
    # have a leaf-style node, we just convert directly to SQL string and push
    # to stack.
    pass
