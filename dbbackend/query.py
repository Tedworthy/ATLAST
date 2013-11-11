import psycopg2
import sys
import csv
import ConfigParser



def query(text):
  con = None
  try:
    config = ConfigParser.RawConfigParser()
    config.read('db.cfg')
    host = config.get('DatabaseCon', 'host')
    port = config.get('DatabaseCon', 'port')
    user  = config.get('DatabaseCon', 'user')
    database = config.get('DatabaseCon', 'dbname')
    password = config.get('DatabaseCon', 'password')
    print "Host: " + host + "\tUser: " + user + "\tPassword: " + port 
    print "Password: " + password + "\tDatabase Name: "+ database
    con = psycopg2.connect('host='+host+' port='+port+' databse='+database+' user='+user +' password='+password)
    cur = con.cursor()
    cur.execute(text)
    result = cur.fetchall()


  except psycopg2.DatabaseError, e:
    result = 'ERROR %s' % e
    
  finally:
    if con:
      con.close()
      return result



result = query("SELECT * FROM films")
print result
