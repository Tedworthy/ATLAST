import xml.etree.ElementTree as ET

class Schema():
  def __init__(self, filename='dbbackend/schema.xml'):
    self._tree = ET.parse(filename)
    self._root = self._tree.getroot()
    self._data = self.gatherTableData()

  def gatherTableData(self):
    # Dictionary for each table.
    big_data = {}

    # For every <table> tag...
    for table in self._root.iter('table'):
      # Table data dictionary. E.g. table[film][primary_keys]
      table_data = {}
      table_name = table.attrib.get('name')
      if table_name is None:
        print 'Error: table tag encountered with no associated name. Skipping.'
        break
      table_data['primary_keys'] = self.gatherPrimaryKeys(table)
      table_data['columns'] = self.gatherColumns(table)
      #table_data[foreign_keys] = getForeignKeys(table) etc...
      big_data[table_name] = table_data

    return big_data

  def gatherPrimaryKeys(self, table):
    values = []
    for primaryKey in table.iter('primaryKey'):
      values.append(primaryKey.text)
    return values

  def gatherColumns(self, table):
    values = []
    for column in table.iter('columnName'):
      values.append(column.text)
    return values

  def getPrimaryKeys(self, table_name):
    table_data = self._data.get(table_name)
    if table_data is None:
      print 'Error: table', table_name, 'not in schema!'
      return None

    return table_data.get('primary_keys')

  def getColumns(self, table_name):
    table_data = self._data.get(table_name)
    if table_data is None:
      print 'Error: table', table_name, 'not in schema!'
      return None

    return table_data.get('columns')

  def getAllData(self):
    return self._data

  def relationAttributeExists(self, relation, attribute):
    table_data = self._data.get(relation)
    if table_data is None:
      return False

    for column in table_data.get('columns'):
      if column == attribute:
        return True

    return False

  def relationExists(self, relation):
    table_data = self._data.get(relation)
    return table_data is not None
