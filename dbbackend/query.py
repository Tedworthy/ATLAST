import sys
import json
import psycopg2

def db():
  return psycopg2.connect(host='axa-prj-03.doc.ic.ac.uk',
                          port='55432', dbname='filmdb',
                          user='link', password='triforce')

def query(query):
    cur = db().cursor()
    cur.execute(query)
    r = [dict((cur.description[i][0], value) \
              for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return r
