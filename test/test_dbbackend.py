from paste.fixture import TestApp
from nose.tools import *
from dbbackend.query import *

class TestBackend():
  def test_parse_config_file_no_file(self):
    config_data = parse_config_file("")
    assert(config_data['Error'] == '1')

  def test_parse_config_file_valid_file(self):
    config_data = parse_config_file('dbbackend/db.cfg')
    assert(config_data['Error'] == '0')

  def test_parse_config_file_invalid_file(self):
    assert(True)
  def test_establish_connection_no_data(self):
    assert(True)
  def test_establish_connection_valid_data(self):
    assert(True)
  def test_establish_connection_invalid_data(self):
    assert(True)
  def test_query_nocon_validdata(self):
    assert(True)
  def test_query_validcon_validdata(self):
    assert(True)
  def test_query_validcon_invaliddata(self):
    assert(True)


