import sys
import json

from celery import Celery

import dbbackend.postgres.postgres_backend as pg
import dbbackend.config_parser as cp

import parsing.parser as p

import codegen.symtable as st
import codegen.ir_generator as irg
import codegen.sql_generator as sg

import semanticanalysis.semantic_analyser as sa

celery = Celery('task', backend='amqp://guest@localhost:5672', broker='amqp://guest@localhost')

@celery.task
def addToProcessingQueue(logic, schema, configData):
  # Set up a response dictionary
  response = {
      'status': '',
      'logic': logic,
      'sql': '',
      'query_columns': [],
      'query_rows': [],
      'error': ''
    }

  # Parse the logic into a logic AST
  try:
   logicAST = p.parse_input(logic)
  except Exception, e:
    print str(e)
    response['status'] = 'parse_error'
    response['error'] = e.getDict()
    return response

  # Generate a symbol table based on the logic AST
  try:
    symbolTable = st.SymTable()
    logicAST.generateSymbolTable(symbolTable)
  except Exception, e:
    # Handle symbol table exception
    response['status'] = 'symtab_error'
    print 'SYMBOLTABLE', str(e)
    return response

  # Run a pass of semantic analysis on the logic AST to check for errors
  try:
    semanticAnalyser = sa.SemanticAnalyser(logicAST, schema)
    semanticAnalyser.analyse()
  except Exception, e:
    # Handle semantic analysis errors
    response['status'] = 'semantic_error'
    response['error'] = e.getDict()
    return response

  # Generate an IR based on the logic AST
  try:
    irGeneratorVisitor = irg.IRGenerator(schema)
    logicAST.accept(irGeneratorVisitor)
  except Exception, e:
    # Handle ir generation errors
    response['status'] = 'irgen_error'
    print 'IRGENERATOR', str(e)
    return response

  # Generate an SQL string based on the above IR
  try:
    sqlGeneratorVisitor = sg.SQLGenerator()
    irGeneratorVisitor.getIR().accept(sqlGeneratorVisitor)
    sql = sqlGeneratorVisitor.getSQL()
  except Exception, e:
    # Handle SQL generation errors
    response['status'] = 'sqlgen_error'
    print 'SQLGENERATOR', str(e)
    return response

  # TODO - Save the config_data to a session variable and use that instead
  # TODO - Check for database connection issues
  # Parse the database config file, open a connection to the database, and
  # finally run the SQL query
  # configData = cp.parse_file('dbbackend/db.cfg')
  con = pg.connect(configData)
  queryResult = pg.query(con, sql)
  con.close()

  # Check if the query ran OK, and set the response either way
  if queryResult['status'] == 'ok':
    response['status'] = 'ok'
    response['sql'] = sql
    response['query_columns'] = queryResult['columns']
    response['query_rows'] = queryResult['rows']
    response['error'] = ''
  else:
    response['status'] = 'db_error'
    response['sql'] = sql
    response['error'] = queryResult['error']

  return response

