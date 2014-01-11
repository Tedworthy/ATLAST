import xml.etree.cElementTree as ET
import lxml.etree as etree
import psycopg2
import dbbackend.postgres.postgres_backend as pg
import dbbackend.config_parser as cp

dbname_query = \
    """
    SELECT current_database() AS dbname
    """

table_query = \
    """
    SELECT table_name
    FROM   information_schema.tables
    WHERE  table_schema = 'public'
  """

primary_key_query = \
  """
    SELECT pg_attribute.attname,
           format_type(pg_attribute.atttypid, pg_attribute.atttypmod)
    FROM   pg_index, pg_class, pg_attribute
    WHERE  pg_class.oid = '%s'::regclass AND
           indrelid = pg_class.oid AND
           pg_attribute.attrelid = pg_class.oid AND
           pg_attribute.attnum = any(pg_index.indkey) AND
           indisprimary
  """

columns_query = \
  """
    SELECT column_name, data_type, ordinal_position
    FROM information_schema.columns
    WHERE table_name = '%s'
    ORDER BY ordinal_position
  """

def generate_db_schema(con):
  # Create schema entries for each table
  tables = pg.query(con, table_query).get('rows')
  if tables is None:
    msg = "ERROR: Tables query returned no data in generate_db_schema."
    print msg
    raise Exception(msg)

  dbname = pg.query(con, dbname_query)['rows'][0][0]
  root = etree.Element("root")
  dbname_node = etree.SubElement(root, "dbname")
  dbname_node.text = dbname

  for table in (table[0] for table in tables):
    # Create a structure with the name of the table
    xmltable = etree.SubElement(root, "table")
    xmltable.set("name", table)

    # Fetch all the primary keys and update the XML accordingly
    keys = pg.query(con, primary_key_query % table)['rows']
    for key in (key[0] for key in keys):
      xml_primary_key = etree.SubElement(xmltable, "primaryKey")
      xml_primary_key.text = key

    # Fetch all the columns and update the XML accordingly
    columns = pg.query(con, columns_query % table)['rows']
    for column in columns:
      xml_column = etree.SubElement(xmltable, "column")
      xml_column.set("name", column[0])
      xml_column_type = etree.SubElement(xml_column, "type")
      xml_column_type.text = column[1]
      xml_column_ordinal = etree.SubElement(xml_column, "ordinal")
      xml_column_ordinal.text = column[2]

  # Write the xml to a file
  tree = ET.ElementTree(root)
  tree.write("dbbackend/schema.xml")

  # TODO add try - catch to catch errors

if __name__ == "__main__":
  config_data = cp.parse_file('dbbackend/db.cfg')
  con = pg.connect(config_data)
  generate_db_schema(con)
