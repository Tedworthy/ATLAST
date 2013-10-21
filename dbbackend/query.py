import psycopg2
import sys

con = None

def query(text):

  try:
  #TODO parse these options from a file 
    con = psycopg2.connect(host='axa-prj-03.doc.ic.ac.uk',
                           port='55432', dbname='filmdb', 
                           user='link', password='triforce')
    cur = con.cursor()
    cur.execute(text)
    query = cur.fetchall()


  except psycopg2.DatabaseError, e:
   query = 'ERROR %s' % e
    
  finally:

    if con:
      con.close()
      return query

