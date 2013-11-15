import web
import time
import os
import parsing.parser
import parsing.task
import json
import parsing
from codegen.symtable import SymTable
from codegen.generic_logic_ast_visitor import GenericLogicASTVisitor
from codegen.sql_generator import SQLGenerator
from dbbackend import query
from dbbackend import schema
from web.wsgiserver import CherryPyWSGIServer

CherryPyWSGIServer.ssl_certificate = './certs/server.crt'
CherryPyWSGIServer.ssl_private_key = './certs/server.key'
render = web.template.render('templates/')

urls = (
  '/', 'index',
  '/schema', 'schematic',
  '/login', 'login'
)

logic_form = web.form.Form(
    web.form.Textarea('logic', class_="box_sizing")
)

login_form = web.form.Form(
    web.form.Textbox('host', class_='textfield',id='port_input'),
    web.form.Textbox('port',class_='textfield',id='port_input'),
    web.form.Textbox('username',class_='textfield',id='username_input'),
    web.form.Password('password',class_='textfield',id='password_input'),
    web.form.Textbox('dbname',class_='textfield',id='dbname_input')
)

class index:
  def GET(self):
    form = logic_form()
    form2 = login_form()
    return render.index(form,form2)

  # TODO: secure the connection, currently it runs everything as root!
  def POST(self):
    # Validates the Form
    form = logic_form()
    form.validates()

    logic_to_translate = form.logic.get_value()

    # RabbitMQ stuff - should work, but commented for the moment until codegen
    # works.
    # Create worker thread and start
    result = parsing.task.add_to_parse_q.delay(logic_to_translate)

    ## Wait for worker thread to finish translation
    while not result.ready():
      time.sleep(0.1)

    ## Get the SQL out of the finished worker thread
    #sql = result.get()

    # Example query there for testing, remove when codegen works
    #sql = "SELECT * FROM casting WHERE part = 'Jason Bourne'"; # Dodgy query

    web.header('Content-Type','text/html; charset=utf-8', unique = True)

    # TODO: This currently overwrites all of the effort made by our RabbitMQ setup!!
    try:
      result = parsing.parse_input(logic_to_translate)
      symbolTable = SymTable()
      codegenVisitor = GenericLogicASTVisitor(web.schema)
      sqlGeneratorVisitor = SQLGenerator()
      result.generateSymbolTable(symbolTable)
      result.accept(codegenVisitor)
      codegenVisitor._IR_stack[0].accept(sqlGeneratorVisitor)
      sql = sqlGeneratorVisitor._sql
      query_result = query.query(sql)
      error = 'ok'
    except Exception, e:
      sql = ''
      query_result = {}
      error = str(e)

    response = {'logic': logic_to_translate, 'error': error, 'sql': sql, 'query': query_result}

    return json.dumps(response)

class schematic:
  def GET(self):
    schema_dict = web.schema.getAllData()
    return json.dumps(schema_dict)

class login:
  def POST(self):
    f = login_form()
    f.validates()
    print f['username']
    print web.input()
    response = {'error' : 'ok'}

    return json.dumps(response)

  def GET(self):
    return "login " 

def is_test():
  if 'WEBPY_ENV' is os.environ:
      return os.environ['WEBPY_ENV'] == 'test'

# Get global vars, create shared global instance of SQLSchema class.
# http://stackoverflow.com/questions/7512681/how-to-keep-a-variable-value-across-requests-in-web-py
web.app = web.application(urls, globals())
web.schema = schema.Schema()

if (not is_test()) and  __name__ == "__main__":
  web.app.run()
