import xml.etree.cElementTree as ET
import lxml.etree as etree
import psycopg2
import dbbackend.postgres.postgres_backend as pg
import dbbackend.config_parser as cp

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
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = '%s'
    ORDER BY ordinal_position
  """

def generate_db_schema(con):
  # Create schema entries for each table
  tables = pg.query(con, table_query)['rows']
  root = etree.Element("root")
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
    for column in (column[0] for column in columns):
      xml_primary_key = etree.SubElement(xmltable, "columnName")
      xml_primary_key.text = column

  # Write the xml to a file
  tree = ET.ElementTree(root)
  tree.write("dbbackend/schema.xml")

  # TODO add try - catch to catch errors

if __name__ == "__main__":
  config_data = cp.parse_file('dbbackend/db.cfg')
  con = pg.connect(config_data)
  generate_db_schema(con)
