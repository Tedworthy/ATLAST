from paste.fixture import TestApp
from nose.tools import *
from code import web

class TestCode():
  def test_index(self):
    middleware=[]
    testApp = TestApp(web.app.wsgifunc(*middleware))
    r = testApp.get('/')
    assert_equal(r.status, 200)
    r.mustcontain('Convert to SQL')

  def test_query(self):
    middleware=[]
    testApp = TestApp(web.app.wsgifunc(*middleware))
    r = testApp.get('/')
    form = r.form['logic']
    print(form.id)
    print(form.action)
    print(form.method)
    form['text'] = 'test'

