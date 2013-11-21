import sys
import json
import psycopg2
import ConfigParser


def parse_config_file(file):
    config_data = {}
    config = ConfigParser.RawConfigParser()
    try:
      config.read(file)
      config_data['host'] = config.get('DatabaseCon', 'host')
      config_data['port'] = config.get('DatabaseCon', 'port')
      config_data['username']  = config.get('DatabaseCon', 'user')
      config_data['dbname'] = config.get('DatabaseCon', 'dbname')
      config_data['password'] = config.get('DatabaseCon', 'password')
    except Exception, e:
        print str(e)
        config_data['Error'] = '1'
    finally:
      return config_data

def establish_connection(config_data):
  con =  psycopg2.connect(host=config_data['host'],
                          port=config_data['port'], 
                          dbname=config_data['dbname'], 
                          user=config_data['username'], 
                          password=config_data['password'])
  return con

def query(con,query):
  result = {
      "status": "",
      "error": "",
      "columns": [],
      "rows": []
    }
  try:
    cur = con.cursor()
    cur.execute(query)
    result["rows"] = cur.fetchall()
    result["columns"] = [desc[0] for desc in cur.description]
    result["status"] = "ok"
  except psycopg2.DatabaseError, e:
    result["error"] = 'ERROR: %s' % e
    result["status"] = "error"
  finally:
    return result
