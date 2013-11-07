import xml.etree.cElementTree as ET
from lxml import etree
import psycopg2

con = psycopg2.connect(host='axa-prj-03.doc.ic.ac.uk',
                       port='55432', dbname='filmdb', 
                       user='link', password='triforce')

table_query = """ SELECT table_name
                  FROM information_schema.tables
                  WHERE table_schema='public'"""

cur = con.cursor()
cur.execute(table_query)
tables = cur.fetchall()

root = etree.Element("root")

for table in (table[0] for table in tables):
  xmltable = etree.SubElement(root, "table")
  xmltable.set("name", table)
  primary_key_query = """ SELECT  pg_attribute.attname,
                                format_type(pg_attribute.atttypid, pg_attribute.atttypmod)
                        FROM    pg_index, pg_class, pg_attribute
                        WHERE   pg_class.oid = '%s'::regclass AND
                                indrelid = pg_class.oid AND
                                pg_attribute.attrelid = pg_class.oid AND
                                pg_attribute.attnum = any(pg_index.indkey) AND 
                                indisprimary""" % table
  cur = con.cursor()
  cur.execute(primary_key_query)
  keys = cur.fetchall()
  for key in (key[0] for key in keys):
    xml_primary_key = etree.SubElement(xmltable, "primaryKey")
    xml_primary_key.text = key

tree = ET.ElementTree(root)
tree.write("schema.xml")
