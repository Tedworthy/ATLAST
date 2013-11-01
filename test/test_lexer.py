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
  def test_true_false(self):
    lex.input(t_TRUE + ' ' + t_FALSE)

    tok = lex.token()
    assert_equal(tok.value, t_TRUE)
    assert_equal(tok.type, TokenEnum().TRUE)

    tok = lex.token()
    assert_equal(tok.value, t_FALSE)
    assert_equal(tok.type, TokenEnum().FALSE)

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

  @with_setup(setup_func, teardown_func)
  def test_implies(self):
    lex.input(t_IMPLIES)
    tok = lex.token()
    assert_equal(tok.value, t_IMPLIES)
    assert_equal(tok.type, TokenEnum().IMPLIES)

    tok = lex.token()
    assert not tok

  @with_setup(setup_func, teardown_func)
  def test_implies(self):
    lex.input(t_IFF)
    tok = lex.token()
    assert_equal(tok.value, t_IFF)
    assert_equal(tok.type, TokenEnum().IFF)

    tok = lex.token()
    assert not tok

  @with_setup(setup_func, teardown_func)
  def test_greater_and_equal_to(self):
    lex.input(t_GT + t_GTE)
    tok = lex.token()
    assert_equal(tok.value, t_GT)
    assert_equal(tok.type, TokenEnum().GT)

    tok = lex.token()
    assert_equal(tok.value, t_GTE)
    assert_equal(tok.type, TokenEnum().GTE)

    tok = lex.token()
    assert not tok

  @with_setup(setup_func, teardown_func)
  def test_less_and_equal_to(self):
    lex.input(t_LT + t_LTE)
    tok = lex.token()
    assert_equal(tok.value, t_LT)
    assert_equal(tok.type, TokenEnum().LT)

    tok = lex.token()
    assert_equal(tok.value, t_LTE)
    assert_equal(tok.type, TokenEnum().LTE)

    tok = lex.token()
    assert not tok

  @with_setup(setup_func, teardown_func)
  def test_eq(self):
    lex.input(t_EQ)
    tok = lex.token()
    assert_equal(tok.value, t_EQ)
    assert_equal(tok.type, TokenEnum().EQ)

    tok = lex.token()
    assert not tok

  @with_setup(setup_func, teardown_func)
  def test_constant(self):
    lex.input('X')
    tok = lex.token()
    assert_equal(tok.value, 'X')
    assert_equal(tok.type, TokenEnum().CONSTANT)

    tok = lex.token()
    assert not tok

  @with_setup(setup_func, teardown_func)
  def test_constant(self):
    lex.input(t_NOT)
    tok = lex.token()
    assert_equal(tok.value, t_NOT)
    assert_equal(tok.type, TokenEnum().NOT)

    tok = lex.token()
    assert not tok

  @with_setup(setup_func, teardown_func)
  def test_identifier_characters(self):
    lex.input('var')
    tok = lex.token()
    assert_equal(tok.value, 'var')
    assert_equal(tok.type, TokenEnum().IDENTIFIER)

    tok = lex.token()
    assert not tok

  @with_setup(setup_func, teardown_func)
  def test_identifier_mixed(self):
    lex.input('var10noise')
    tok = lex.token()
    assert_equal(tok.value, 'var10noise')
    assert_equal(tok.type, TokenEnum().IDENTIFIER)

    tok = lex.token()
    assert not tok

  @with_setup(setup_func, teardown_func)
  def test_identifier_stringlit(self):
    lex.input('\'stringliteral\'')
    tok = lex.token()
    assert_equal(tok.value, 'stringliteral')
    assert_equal(tok.type, TokenEnum().STRINGLIT)

    tok = lex.token()
    assert not tok

  @with_setup(setup_func, teardown_func)
  def test_identifier_ignore(self):
    lex.input('              ')
    tok = lex.token()
    assert not tok

