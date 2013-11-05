from source import Source

class TableSource(Source):

  def __init__(self, table_name):
    self.table_name = table_name
    self.alias = None

  def __init__(self, table_name, alias):
    self.table_name = table_name
    self.alias = alias

