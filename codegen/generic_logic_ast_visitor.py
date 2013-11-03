'''
Generic Logic AST Visitor
This class implements the visitor pattern over the AST, converting it to a
generic intermediate representation for code generation.
'''

import visit as v
import ast

class GenericLogicASTVisitor():

  def __init__(self):
    # Instance variables go here, if necessary
    pass

  @v.on('node')
  def visit(self, node):
    # Generic node, don't think you're supposed to change this
    pass

  @v.when(ast.IffNode)
  def visit(self, node):
    print "Seen IffNode"
    map(self.visit, node.getChildren())

  @v.when(ast.OrNode)
  def visit(self, node):
    print "Seen OrNode"
    map(self.visit, node.getChildren())

  @v.when(ast.AndNode)
  def visit(self, node):
    print "Seen AndNode"
    map(self.visit, node.getChildren())

  @v.when(ast.NotNode)
  def visit(self, node):
    print "Seen NotNode"
    map(self.visit, node.getChildren())

  @v.when(ast.ForAllNode)
  def visit(self, node):
    print "Seen ForAllNode"
    map(self.visit, node.getChildren())

  @v.when(ast.ThereExistsNode)
  def visit(self, node):
    print "Seen ThereExistsNode"
    map(self.visit, node.getChildren())

  @v.when(ast.PredicateNode)
  def visit(self, node):
    print "Seen PredicateNode"
    map(self.visit, node.getChildren())

  @v.when(ast.BinaryEqualityNode)
  def visit(self, node):
    print "Seen BinaryEqualityNode"
    map(self.visit, node.getChildren())

  @v.when(ast.FunctionNode)
  def visit(self, node):
    print "Seen FunctionNode"
    map(self.visit, node.getChildren())

  @v.when(ast.ConstantNode)
  def visit(self, node):
    print "Seen ConstantNode"
    map(self.visit, node.getChildren())

  @v.when(ast.VariableNode)
  def visit(self, node):
    print "Seen VariableNode"
    map(self.visit, node.getChildren())

