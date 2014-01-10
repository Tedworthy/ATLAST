import xml.etree.ElementTree as ET

class Schema():
  def __init__(self, filename='dbbackend/schema.xml'):
    self._tree = ET.parse(filename)
    self._root = self._tree.getroot()
    self._data = self.gatherTableData()

  def gatherTableData(self):
    # Dictionary for each table.
    schema_dict = {}
    schema_dict["tables"] = {}
    schema_dict["dbname"] = self._root.find("dbname").text

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
      schema_dict["tables"][table_name] = table_data

    return schema_dict

  def gatherPrimaryKeys(self, table):
    values = []
    for primaryKey in table.iter('primaryKey'):
      values.append(primaryKey.text)
    return values

  def gatherColumns(self, table):
    values = {}
    for column in table.iter('column'):
      column_vals = {}
      column_vals['type'] = column.find('type').text
      values[column.attrib.get('name')] = column_vals
    return values

  def getPrimaryKeys(self, table_name):
    table_data = self._data["tables"].get(table_name)
    if table_data is None:
      print 'Error: table', table_name, 'not in schema!'
      return None

    return table_data.get('primary_keys')

  def getColumns(self, table_name):
    table_data = self._data["tables"].get(table_name)
    if table_data is None:
      print 'Error: table', table_name, 'not in schema!'
      return None

    columns = table_data.get('columns') or {}
    result = []

    for column_name in columns.keys():
      result.append(column_name)

    return result

  def getColumnType(self, table_name, column_name):
    table_data = self._data["tables"].get(table_name)
    if table_data is None:
      print 'Error: table', table_name, 'not in schema!'
      return None

    columns = table_data.get('columns') or {}
    column = columns.get('column_name')

    if column is None:
      print 'Error: table', table_name, 'has no column', column_name
      return None

    return column.get('type')

  def getAllData(self):
    return self._data

  def relationAttributeExists(self, relation, attribute):
    table_data = self._data["tables"].get(relation)
    if table_data is None:
      return False

    for column in table_data.get('columns'):
      if column == attribute:
        return True

    return False

  def relationExists(self, relation):
    table_data = self._data["tables"].get(relation)
    return table_data is not None
