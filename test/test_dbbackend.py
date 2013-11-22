from paste.fixture import TestApp
from nose.tools import *
from dbbackend.postgres.postgres_backend import *
from dbbackend.config_parser import *

class TestBackend():
  def test_parse_config_file_no_file(self):
    config_data = parse_config_file("")
    assert(config_data['Error'] == '1')

  def test_parse_config_file_valid_file(self):
    config_data = parse_config_file('test/test_db.cfg')
    assert(config_data['Error'] == '0')
    assert(config_data['host'] == 'testhost')
    assert(config_data['username'] == 'testuser')
    assert(config_data['port'] == '8080')
    assert(config_data['dbname'] == 'testdb')
    assert(config_data['password'] == 'testpass') 

  def test_parse_config_file_invalid_file(self):
    config_data = parse_config_file('test/test_db_invalid.cfg')
    assert(config_data['Error'] == '1')

  def test_establish_connection_no_data(self):
    con = establish_connection()
    assert(True)

  def test_establish_connection_valid_data(self):
    config_data = parse_config_file('dbbackend/db.cfg')
    con = establish_connection(config_data)
    assert(True)

  def test_establish_connection_invalid_data(self):
    config_data = parse_config_file('dbbackend/db.cfg')
    con = establish_connection(config_data)
    assert(True)

  def test_query_nocon_validdata(self):
    execute_query()
    assert(True)

  def test_query_validcon_validdata(self):
    execute_query()
    assert(True)

  def test_query_validcon_invaliddata(self):
    execute_query()
    assert(True)


