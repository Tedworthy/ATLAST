# -*- coding=utf-8 -*-
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

from dbbackend import schema

import dbbackend.generate_schema as gs
import dbbackend.postgres.postgres_backend as pg
import dbbackend.config_parser as cp

from web.wsgiserver import CherryPyWSGIServer

CherryPyWSGIServer.ssl_certificate = './certs/server.crt'
CherryPyWSGIServer.ssl_private_key = './certs/server.key'
render = web.template.render('templates/')

urls = (
  '/', 'index',
  '/schema', 'db_schema',
  '/login', 'login',
  '/tables', 'tables'
)

logic_form = web.form.Form(
    web.form.Textarea('logic', class_="box_sizing")
)

login_form = web.form.Form(
    web.form.Textbox('host', class_='textfield',id='host_input'),
    web.form.Textbox('port',class_='textfield',id='port_input'),
    web.form.Textbox('username',class_='textfield',id='username_input'),
    web.form.Password('password',class_='textfield',id='password_input'),
    web.form.Textbox('dbname',class_='textfield',id='dbname_input'),
    web.form.Button('Connect', id='config_submit')
)

class index:
  def GET(self):
    web.header('Content-Type','text/html; charset=utf-8', unique = True)
    logicForm = logic_form()
    loginForm = login_form()
    return render.index(logicForm,loginForm)

  # TODO: secure the connection, currently it runs everything as root!
  def POST(self):
    # Validates the Form
    logicForm = logic_form()
    logicForm.validates()

    logic_to_translate = logicForm.logic.get_value()

    # Create worker thread and start (CURRENTLY POINTLESS - see later comment)
    result = parsing.task.add_to_parse_q.delay(logic_to_translate)

    # Wait for worker thread to finish translation
    while not result.ready():
      time.sleep(0.1)

    web.header('Content-Type','application/json; charset=utf-8', unique = True)

    # Set up a response dictionary
    response = {
        'status': '',
        'logic': logic_to_translate,
        'sql': '',
        'query_columns': [],
        'query_rows': [],
        'error': ''
      }

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
     
        #TODO - Save the config_data to a session variable and use that instead
        config_data = cp.parse_file('dbbackend/db.cfg')
        con = pg.connect(config_data)
        query_result = pg.query(con, sql)

        if query_result['status'] == 'ok':
          response['status'] = 'ok'
          response['sql'] = sql
          response['query_columns'] = query_result['columns']
          response['query_rows'] = query_result['rows']
        else:
          response['status'] = 'db_error'
          response['error'] = query_result['error']

        con.close()
    except Exception, e:
      response['status'] = 'exception_error'
      print e
      response['error'] = 'ERROR: %s' % str(e)

    return json.dumps(response)

class db_schema:
  def GET(self):
    web.header('Content-Type','application/json; charset=utf-8', unique = True)
    schema_dict = web.schema.getAllData()
    return json.dumps(schema_dict)

class tables:
  def GET(self):
    web.header('Content-Type','text/html; charset=utf-8', unique = True)
    return render.tables()

class login:
  def POST(self):
    try:
      f = login_form()
      f.validates()

      config_data =  web.input()
      print config_data

      # TODO: Validate user input
      generate_schema.generate_db_schema(config_data)
      # TODO: store in session variable not global variable
      web.schema = schema.Schema()
      web.header('Content-Type','application/json; charset=utf-8', unique=True)
      response = {'error' : 'ok', 'Content-Type' : 'text/plain'}
      return json.dumps(response)

    except Exception, error:
      print 'Login failed'
      print str(error)
      return json.dumps({'error' : str(error)})

  def GET(self):
    web.header('Content-Type','application/json; charset=utf-8', unique = True)
    response = {'error' : 'ok', 'Content-Type' : 'text/plain'}
    return json.dumps(response)

def is_test():
  if 'WEBPY_ENV' is os.environ:
      return os.environ['WEBPY_ENV'] == 'test'

web.app = web.application(urls, globals())

if (not is_test()) and  __name__ == "__main__":
  gs.generate_db_schema(pg.connect(cp.parse_file('dbbackend/db.cfg')))
  web.app.run()

# Get global vars, create shared global instance of SQLSchema class.
# http://stackoverflow.com/questions/7512681/how-to-keep-a-variable-value-across-requests-in-web-py
web.schema = schema.Schema()

