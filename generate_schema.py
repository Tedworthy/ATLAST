import xml.etree.cElementTree as ET
from lxml import etree
import psycopg2
from dbbackend.query import *

table_query = """ SELECT table_name
                  FROM information_schema.tables
                  WHERE table_schema='public'"""

primary_key_query = """ SELECT  pg_attribute.attname,
                              format_type(pg_attribute.atttypid, pg_attribute.atttypmod)
                      FROM    pg_index, pg_class, pg_attribute
                      WHERE   pg_class.oid = '%s'::regclass AND
                              indrelid = pg_class.oid AND
                              pg_attribute.attrelid = pg_class.oid AND
                              pg_attribute.attnum = any(pg_index.indkey) AND 
                              indisprimary""" 

columns_query = """ SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name = '%s' """ 




def generate_db_schema(config_data):
  con = establish_connection(config_data)
  tables = query(con,table_query)['rows']
  root = etree.Element("root")
  for table in (table[0] for table in tables):
    # Create a structure with the name of the table
    xmltable = etree.SubElement(root, "table")
    xmltable.set("name", table)
    keys = query(con,primary_key_query % table)['rows']
    
    for key in (key[0] for key in keys):
      xml_primary_key = etree.SubElement(xmltable, "primaryKey")
      xml_primary_key.text = key
    
    columns = query(con,columns_query % table)['rows']

    for column in (column[0] for column in columns):
      xml_primary_key = etree.SubElement(xmltable, "columnName")
      xml_primary_key.text = column
  con.close()
  # Write the xml to a file
  tree = ET.ElementTree(root)
  tree.write("schema.xml")
# add try - catch to catch errors

if __name__ == "__main__":
  generate_db_schema(parse_config_file('dbbackend/db.cfg'))
