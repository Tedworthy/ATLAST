# -*- coding=utf-8 -*-

import web
import time
import os
import json
import task as worker

from dbbackend import schema

import dbbackend.generate_schema as gs
import dbbackend.postgres.postgres_backend as pg
import dbbackend.config_parser as cp

from web.wsgiserver import CherryPyWSGIServer

CherryPyWSGIServer.ssl_certificate = './certs/server.crt'
CherryPyWSGIServer.ssl_private_key = './certs/server.key'
render = web.template.render('templates/')

urls = (
  '/', 'Index',
  '/schema', 'DBSchema',
  '/login', 'Login',
  '/tables', 'Tables'
)

#logicForm = web.form.Form(
#    web.form.Textarea('logic')
#)

settingsForm = web.form.Form(
    web.form.Textbox('host', class_='textfield', id='host_input'),
    web.form.Textbox('port', class_='textfield', id='port_input'),
    web.form.Textbox('username', class_='textfield', id='username_input'),
    web.form.Password('password', class_='textfield', id='password_input'),
    web.form.Textbox('dbname', class_='textfield', id='dbname_input'),
    web.form.Button('Connect', id='config_submit')
)

class Index:
  def GET(self):
    web.header('Content-Type', 'text/html; charset=utf-8', unique = True)
    #logic = logicForm()
    settings = settingsForm()
    return render.index(settings)

  # TODO: secure the connection, currently it runs everything as root!
  def POST(self):
    logic = web.input().logic

    # Create worker thread and start
    result = worker.addToProcessingQueue.delay(logic, web.schema)

    # Wait for worker thread to finish processing
    while not result.ready():
      time.sleep(0.1)

    # Get the result from the worker thread
    response = result.get()

    web.header('Content-Type','application/json; charset=utf-8', unique = True)
    return json.dumps(response)

class DBSchema:
  def GET(self):
    schema = web.schema.getAllData()
    web.header('Content-Type','application/json; charset=utf-8', unique = True)
    return json.dumps(schema)

class Tables:
  def GET(self):
    web.header('Content-Type','text/html; charset=utf-8', unique = True)
    return render.tables()

class Login:
  def GET(self):
    response = {
        'error': 'ok',
        'Content-Type': 'text/plain'
      }
    web.header('Content-Type','application/json; charset=utf-8', unique = True)
    return json.dumps(response)

  def POST(self):
    response = {
        'error': '',
        'Content-Type': 'text/plain'
      }
    try:
      settings = settingsForm()
      settings.validates()

      configData = web.input()
      print configData

      # TODO: Validate user input
      gs.generate_db_schema(configData)
      # TODO: store in session variable not global variable
      web.schema = schema.Schema()

      response['error'] = 'ok'
    except Exception, e:
      print 'Login failed'
      print str(e)
      response['error'] = str(e)

    web.header('Content-Type','application/json; charset=utf-8', unique=True)
    return json.dumps(response)

def isTest():
  if 'WEBPY_ENV' is os.environ:
    return os.environ['WEBPY_ENV'] == 'test'
  else:
    return False

# TODO: Get global vars, create shared global instance of SQLSchema class.
# http://stackoverflow.com/questions/7512681/how-to-keep-a-variable-value-across-requests-in-web-py
web.schema = schema.Schema()
web.app = web.application(urls, globals())

if (not isTest()) and  __name__ == "__main__":
  gs.generate_db_schema(pg.connect(cp.parse_file('dbbackend/db.cfg')))
  web.app.run()

