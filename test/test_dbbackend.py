from paste.fixture import TestApp
from nose.tools import *
import dbbackend.postgres.postgres_backend as pg
import dbbackend.config_parser as cp

class TestBackend():
  def test_parse_config_file_no_file(self):
    config_data = cp.parse_file("")
    assert(config_data['error'] == '1')

  def test_parse_config_file_valid_file(self):
    config_data = cp.parse_file('test/db_valid.cfg')
    assert(config_data['error'] == '0')
    assert(config_data['host'] == 'testhost')
    assert(config_data['username'] == 'testuser')
    assert(config_data['port'] == '8080')
    assert(config_data['dbname'] == 'testdb')
    assert(config_data['password'] == 'testpass') 

  def test_parse_config_file_invalid_file(self):
    config_data = cp.parse_file('test/db_invalid.cfg')
    assert(config_data['error'] == '1')

  def test_establish_connection_no_data(self):
    con = pg.connect(None)
    assert(True)

  def test_establish_connection_valid_data(self):
    config_data = cp.parse_file('dbbackend/db.cfg')
    con = pg.connect(config_data)
    assert(True)

  def test_establish_connection_invalid_data(self):
    config_data = cp.parse_file('dbbackend/db.cfg')
    con = pg.connect(config_data)
    assert(True)

  def test_query_nocon_validdata(self):
    pg.query(None,'SELECT * FROM films')
    assert(True)

  def test_query_validcon_validdata(self):
    config_data = cp.parse_file('dbbackend/db.cfg')
    con = pg.connect(config_data)
    pg.query(con,'SELECT * FROM films')
    assert(True)

  def test_query_validcon_invaliddata(self):
    config_data = cp.parse_file('dbbackend/db.cfg')
    con = pg.connect(config_data)
    pg.query(con,'ADSFS')
    assert(True)
