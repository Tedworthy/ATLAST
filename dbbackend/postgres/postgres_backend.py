import sys
import json
import psycopg2

def establish_connection(config_data):
  con =  psycopg2.connect(host=config_data['host'],
                          port=config_data['port'], 
                          dbname=config_data['dbname'], 
                          user=config_data['username'], 
                          password=config_data['password'])
  return con

def execute_query(con,query):
  result = {
      "status": "",
      "error": "",
      "columns": [],
      "rows": []
    }
  try:
    cur = con.cursor()
    cur.execute(query)
    result['rows'] = cur.fetchall()
    result['columns'] = [desc[0] for desc in cur.description]
    result['status'] = "ok"
  except psycopg2.DatabaseError, e:
    result['error'] = 'ERROR: %s' % e
    result['status'] = "error"
  finally:
    return result
