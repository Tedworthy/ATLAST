from paste.fixture import TestApp
from nose.tools import *
from code import app
from parsing.lexer import *

class TestCode():
  def test_index(self):
    middleware=[]
    testApp = TestApp(app.wsgifunc(*middleware))
    r = testApp.get('/')
    assert_equal(r.status, 200)
    r.mustcontain('Convert to SQL')

  def test_query(self):
    middleware=[]
    testApp = TestApp(app.wsgifunc(*middleware))
    r = testApp.get('/')
    form = r.forms['logic-form']
    print(form.id)
    form['logic'] = t_THEREEXISTS.encode('utf-8') + 'x(film_title(x))'
    r = form.submit()
    assert_equal(r.status, 200)
    r.mustcontain( t_THEREEXISTS.encode('utf-8') + 'x(film_title(x))')
