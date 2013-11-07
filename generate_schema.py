import psycopg2

table_query = """ SELECT table_name
                  FROM information_schema.tables
                  WHERE table_schema='public'"""

con = psycopg2.connect(host='axa-prj-03.doc.ic.ac.uk',
                       port='55432', dbname='filmdb', 
                       user='link', password='triforce')
cur = con.cursor()
cur.execute(table_query)
tables = cur.fetchall()

for table in (table[0] for table in tables):
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
  print keys
