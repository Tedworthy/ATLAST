from paste.fixture import TestApp
from nose.tools import *
from code import web
from parsing.lexer import *

class TestEndToEnd():
  def test_end_to_end(self):
    middleware=[]
    testApp = TestApp(web.app.wsgifunc(*middleware))
    r = testApp.get('/')
    form = r.forms['logic-form']
    print(form.id)
    form['logic'] = t_THEREEXISTS.encode('utf-8') + 'x(film_title(x))'
    r = form.submit()
    assert_equal(r.status, 200)
    r.mustcontain('SELECT title FROM film')
