from source import Source

class JoinSource(Source):

  def __init__(self, join_type, source1, source2, join_constraints):
    self.join_type = join_type
    self.source1 = source1
    self.source2 = source2
    self.join_constraints = join_constraints
