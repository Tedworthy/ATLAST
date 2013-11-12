from parsing.lexer import *
from paste.fixture import TestApp
from nose.tools import *

class TestLexer():

  def setup_func():
    "Set up lexer"
    lex.lex()

  def teardown_func():
    "Tears down lexer"

  @with_setup(setup_func, teardown_func)
  def test_forall(self):
    lex.input(t_FORALL + 'x()')
    tok = lex.token()
    print tok
    assert_equal(tok.value, t_FORALL)
    assert_equal(tok.type, TokenEnum().FORALL)

  @with_setup(setup_func, teardown_func)
  def test_thereexists(self):
    lex.input(t_THEREEXISTS + 'x()')
    tok = lex.token()
    assert_equal(tok.value, t_THEREEXISTS)
    assert_equal(tok.type, TokenEnum().THEREEXISTS)

    tok = lex.token()
    assert_equal(tok.value, 'x')
    assert_equal(tok.type, TokenEnum().IDENTIFIER)

    tok = lex.token()
    assert_equal(tok.value, '(')
    assert_equal(tok.type, TokenEnum().LBRACKET)

    tok = lex.token()
    assert_equal(tok.value, ')')
    assert_equal(tok.type, TokenEnum().RBRACKET)

    tok = lex.token()
    assert not tok

  @with_setup(setup_func, teardown_func)
  def test_predicate(self):
    lex.input('p(x)')
    tok = lex.token()
    assert_equal(tok.value, 'p')
    assert_equal(tok.type, TokenEnum().IDENTIFIER)

    tok = lex.token()
    assert_equal(tok.value, '(')
    assert_equal(tok.type, TokenEnum().LBRACKET)

    tok = lex.token()
    assert_equal(tok.value, 'x')
    assert_equal(tok.type, TokenEnum().IDENTIFIER)

    tok = lex.token()
    assert_equal(tok.value, ')')
    assert_equal(tok.type, TokenEnum().RBRACKET)

    tok = lex.token()
    assert not tok

  @with_setup(setup_func, teardown_func)
  def test_predicate_list(self):
    lex.input('p(x, y)')
    tok = lex.token()
    assert_equal(tok.value, 'p')
    assert_equal(tok.type, TokenEnum().IDENTIFIER)

    tok = lex.token()
    assert_equal(tok.value, '(')
    assert_equal(tok.type, TokenEnum().LBRACKET)

    tok = lex.token()
    assert_equal(tok.value, 'x')
    assert_equal(tok.type, TokenEnum().IDENTIFIER)

    tok = lex.token()
    assert_equal(tok.value, ',')
    assert_equal(tok.type, TokenEnum().COMMA)

    tok = lex.token()
    assert_equal(tok.value, 'y')
    assert_equal(tok.type, TokenEnum().IDENTIFIER)

    tok = lex.token()
    assert_equal(tok.value, ')')
    assert_equal(tok.type, TokenEnum().RBRACKET)

    tok = lex.token()
    assert not tok

  @with_setup(setup_func, teardown_func)
  def test_and(self):
    lex.input(t_AND)
    tok = lex.token()
    assert_equal(tok.value, t_AND)
    assert_equal(tok.type, TokenEnum().AND)

    tok = lex.token()
    assert not tok

  @with_setup(setup_func, teardown_func)
  def test_or(self):
    lex.input(t_OR)
    tok = lex.token()
    assert_equal(tok.value, t_OR)
    assert_equal(tok.type, TokenEnum().OR)

    tok = lex.token()
    assert not tok

