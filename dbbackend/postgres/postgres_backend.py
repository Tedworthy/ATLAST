import psycopg2

def connect(config_data):
  try:
    con = psycopg2.connect(host=config_data['host'],
                           port=config_data['port'],
                           database=config_data['dbname'],
                           user=config_data['username'],
                           password=config_data['password'])
  except Exception, e:
    return 'ERROR'
  return con

def query(con, query):
  result = {}
  try:
    cur = con.cursor()
    cur.execute(query)

    # Convert all rows to string representation
    result['rows'] = []
    for row in cur.fetchall():
      result_row = []
      for val in row:
        result_row.append(str(val))
      result['rows'].append(result_row)

#    result['rows'] = cur.fetchall()
    result['columns'] = [desc[0] for desc in cur.description]
    result['status'] = 'ok'
  except psycopg2.DatabaseError, e:
    result['error'] = str(e)
    result['status'] = 'db_error'
  finally:
    return result
