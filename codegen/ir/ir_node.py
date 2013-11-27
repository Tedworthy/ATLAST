class IRNode():

  def __init__(self):
    pass

  def accept(self, visitor):
    visitor.visit(self)


