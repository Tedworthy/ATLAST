from paste.fixture import TestApp
from nose.tools import *
from codegen import symtable

class TestSymbolTable():
  def test_insertions(self):
    table = SymTable()
    table.addItem(1,"Joe")
    assert_equal(table._data[1], "Joe")
    
  def test_retrievals_local(self):
    table = SymTable()
    table.addItem(1,"Joe")
    assert_equal(table.lookup(1), "Joe")


  def test_setParent(self):
    table = SymTable()
    table.setParent(SymTable())
    assert table._parent is not None

  def test_hasParent(self):
    table = SymTable()
    table._parent = SymTable()
    assert(table.hasParent())

  def test_getParent(self):
    table = SymTable()
    table._parent = SymTable()
    assert table.getParent() is not None

  def test_addGlobal_at_Global(self):
    table = SymTable()
    table.addItem(1,"Joe")
    assert_equal(table._data[1], "Joe")


  def test_addGlobal_at_Local(self):
    table = SymTable()
    table.addItem(1,"Joe")
    assert_equal(table._data[1], "Joe")




