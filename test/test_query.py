from paste.fixture import TestApp
from nose.tools import *
from code import app
from parsing.lexer import *

class TestQuery():
  def test_query(self):
    middleware=[]
    testApp = TestApp(app.wsgifunc(*middleware))
    r = testApp.get('/')
    form = r.forms['logic-form']
    print(form.id)
    form['logic'] = t_THEREEXISTS.encode('utf-8') + 'x(film_title(x))'
    r = form.submit()
    assert_equal(r.status, 200)
    r.mustcontain('SELECT title FROM film')
