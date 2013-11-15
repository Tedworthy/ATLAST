import xml.etree.cElementTree as ET
from lxml import etree
import psycopg2

# Establish the connection
con = psycopg2.connect(host='axa-prj-03.doc.ic.ac.uk',
                       port='55432', dbname='filmdb', 
                       user='link', password='triforce')

# postgreSQL query to get all table names in a db
table_query = """ SELECT table_name
                  FROM information_schema.tables
                  WHERE table_schema='public'"""

# Execute the query
cur = con.cursor()
cur.execute(table_query)
tables = cur.fetchall()

# Build the root of an xml structure
root = etree.Element("root")

# Iterate over the tables
for table in (table[0] for table in tables):

  # Create a structure with the name of the table
  xmltable = etree.SubElement(root, "table")
  xmltable.set("name", table)

  # Query to retrieve all primary keys from a given table
  primary_key_query = """ SELECT  pg_attribute.attname,
                                format_type(pg_attribute.atttypid, pg_attribute.atttypmod)
                        FROM    pg_index, pg_class, pg_attribute
                        WHERE   pg_class.oid = '%s'::regclass AND
                                indrelid = pg_class.oid AND
                                pg_attribute.attrelid = pg_class.oid AND
                                pg_attribute.attnum = any(pg_index.indkey) AND 
                                indisprimary""" % table

  # Execute the primary key query (TODO refactor, dat code duplication)
  cur = con.cursor()
  cur.execute(primary_key_query)
  keys = cur.fetchall()

  # Iterate through all the keys returned, and add them to the table structure
  for key in (key[0] for key in keys):
    xml_primary_key = etree.SubElement(xmltable, "primaryKey")
    xml_primary_key.text = key
  
  columns_query = """ SELECT column_name
                      FROM information_schema.columns
                      WHERE table_name = '%s' """ % table
  
  # Execute the primary key query (TODO refactor, dat code duplication)
  cur = con.cursor()
  cur.execute(columns_query)
  keys = cur.fetchall()

  # Iterate through all the keys returned, and add them to the table structure
  for key in (key[0] for key in keys):
    xml_primary_key = etree.SubElement(xmltable, "columnName")
    xml_primary_key.text = key

# Write the xml to a file
tree = ET.ElementTree(root)
tree.write("schema.xml")
