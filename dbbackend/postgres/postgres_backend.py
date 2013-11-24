import psycopg2

def connect(config_data):
  con = psycopg2.connect(host=config_data['host'],
                         port=config_data['port'],
                         database=config_data['dbname'],
                         user=config_data['username'],
                         password=config_data['password'])
  return con

def query(con, query):
  result = {}
  try:
    cur = con.cursor()
    cur.execute(query)
    result['rows'] = cur.fetchall()
    result['columns'] = [desc[0] for desc in cur.description]
    result['status'] = 'ok'
  except psycopg2.DatabaseError, e:
    result['error'] = str(e)
    result['status'] = 'db_error'
  finally:
    return result
