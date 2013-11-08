import web
import time
import os
import parsing.parser
import parsing.task
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

  def POST(self):
    form = logic_form()
    # Validates the Form
    form.validates()
    # TODO: We have the logic as a string, we need to process it
    logic_to_translate = form.logic.get_value()
    # translated = query.query(logic_to_translate) TODO secure the connection
    # currently it runs everything as root which is LOLZ 
    web.header('Content-Type','text/html; charset=utf-8', unique=True) 
    result = parsing.task.add_to_parse_q.delay(logic_to_translate)
    while not result.ready():
      time.sleep(0.1) #TODO remove busy waiting, semaphore/callback this bitch
    return json.dumps({'sql': logic_to_translate, 'query': 'A result! Yay...'})

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
