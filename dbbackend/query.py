import sys
import json
import psycopg2
import ConfigParser



def query(text):
  con = None
  result = {
      "status": "",
      "error": "",
      "columns": [],
      "rows": []
    }
  try:
    config = ConfigParser.RawConfigParser()
    config.read('dbbackend/db.cfg')
    host = config.get('DatabaseCon', 'host')
    port = config.get('DatabaseCon', 'port')
    user  = config.get('DatabaseCon', 'user')
    database = config.get('DatabaseCon', 'dbname')
    password = config.get('DatabaseCon', 'password')
    print "Host: " + host + "\tUser: " + user + "\tPassword: " + port 
    print "Password: " + password + "\tDatabase Name: "+ database
    con = psycopg2.connect('host='+host+' port='+port+' dbname='+database+' user='+user +' password='+password)
    cur = con.cursor()
    cur.execute(text)
    result["rows"] = cur.fetchall()
    result["columns"] = [desc[0] for desc in cur.description]
    result["status"] = "ok"
  except psycopg2.DatabaseError, e:
    result["error"] = 'ERROR: %s' % e
    result["status"] = "error"
  finally:
    if con:
      con.close()
    return result
