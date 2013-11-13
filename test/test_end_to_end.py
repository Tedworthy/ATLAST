# -*- coding: utf-8 -*-
from paste.fixture import TestApp
from nose.tools import *
from code import web
from parsing.lexer import *

class TestEndToEnd():

  def setup_func():
    pass

  def teardown_func():
    pass

  def test_end_to_end(self):
    middleware=[]
    testApp = TestApp(web.app.wsgifunc(*middleware))
    r = testApp.get('/')
    form = r.forms['logic-form']
    print(form.id)
    form['logic'] = '∃x(films_title(x, y) ∧ films_director(x, z))'
    #form['logic'] = t_THEREEXISTS.encode('utf-8') + 'x(film_title(x, y))'
    r = form.submit()
    assert_equal(r.status, 200)
    print r
    r.mustcontain("SELECT films.title, films.director FROM films")
