import sys
import json
import psycopg2
import ConfigParser

def db():
  con = None
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
    return psycopg2.connect('host='+host+' port='+port+' dbname='+database+' user='+user +' password='+password)
  except Exception, e:
    raise e

        
        

def run_query(sql):
    cur = db().cursor()
    try:
      cur.execute(sql)
      r = [dict((cur.description[i][0], value) \
              for i, value in enumerate(row)) for row in cur.fetchall()]
    except Exception, e:
      cur.connection.close()
      raise e
    
    return r
