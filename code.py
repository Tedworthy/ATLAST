import web
import os
import json
from dbbackend import query

render = web.template.render('templates/')

urls = (
  '/', 'index'
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
    # TODO: secure the connection, currently it runs everything as root!
    #translated = query.query(logic_to_translate)
    web.header('Content-Type','text/html; charset=utf-8', unique=True)
    sql = "SELECT * FROM casting WHERE part = 'Jason Bourne'";
    query_result = query.query(sql)
    response = {'sql': sql, 'query': query_result}
    
    print json.dumps(response)  
    
    return json.dumps(response)

def is_test():
  if 'WEBPY_ENV' is os.environ:
      return os.environ['WEBPY_ENV'] == 'test'

app = web.application(urls, globals())

if (not is_test()) and  __name__ == "__main__":
  app.run()

