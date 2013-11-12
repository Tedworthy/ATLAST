import web
import os
import json
from dbbackend import query
from dbbackend import schema

render = web.template.render('templates/')

urls = (
  '/', 'index'
  '/schema', 'schematic'
)

logic_form = web.form.Form(
    web.form.Textarea('logic', class_="box_sizing")
)

class index:
  def GET(self):
    form = logic_form()
    return render.index(form)

  # TODO: secure the connection, currently it runs everything as root!
  def POST(self):
    # Validates the Form
    form = logic_form()
    form.validates()

    logic_to_translate = form.logic.get_value()
    web.header('Content-Type','text/html; charset=utf-8', unique=True)

    # RabbitMQ stuff - should work, but commented for the moment until codegen
    # works.
    # Create worker thread and start
    #result = parsing.task.add_to_parse_q.delay(logic_to_translate)

    ## Wait for worker thread to finish translation
    #while not result.ready():
    #  time.sleep(0.1)

    ## Get the SQL out of the finished worker thread
    #sql = result.get()

    # Example query there for testing, remove when codegen works
    sql = "SELECT * FROM casting WHERE pqrt = 'Jason Bourne'"; # Dodgy query

    try:
      query_result = query.run_query(sql)
      error = 'ok'
    except Exception, e:
      query_result = {}
      error = str(e)

    response = {'error': error, 'sql': sql, 'query': query_result}

    return json.dumps(response)

class schematic:
  def GET(self):
    schema_dict = web.schema.getAllData()
    return json.dumps(schema_dict)

def is_test():
  if 'WEBPY_ENV' is os.environ:
      return os.environ['WEBPY_ENV'] == 'test'

# Get global vars, create shared global instance of SQLSchema class.
# http://stackoverflow.com/questions/7512681/how-to-keep-a-variable-value-across-requests-in-web-py
web.app = web.application(urls, globals())
web.schema = schema.Schema()

if (not is_test()) and  __name__ == "__main__":
  web.app.run()
