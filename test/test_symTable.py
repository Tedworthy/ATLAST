from paste.fixture import TestApp
from nose.tools import *
from codegen.symtable import SymTable

class TestSymbolTable():
  def test_insertions(self):
    table = SymTable()
    table.addItem(1,"Joe")
    assert_equal(table._data[1], "Joe")

  def test_retrievals_local(self):
    table = SymTable()
    table.addItem(1,"Joe")
    assert_equal(table.lookup(1), "Joe")

  def test_retrievals_global(self):
    table = SymTable()
    childTable = SymTable(table)
    childTable.addGlobal(1,"Joe")
    assert_equal(childTable.lookup(1), "Joe")

  def test_retrievals_not_exists_global(self):
    table = SymTable()
    assert_not_equal(table.lookup(1), "Joe")

  def test_default_constructor(self):
    table = SymTable()
    assert_equal( table._parent, None)
    assert_equal( table._data, {})

  def test_set_parent_in_constructor(self):
    table = SymTable(SymTable())
    assert table._parent is not None

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
    table.addGlobal(1,"Joe")
    assert_equal(table._data[1], "Joe")


  def test_addGlobal_at_Local(self):
    table = SymTable()
    childTable = SymTable(table)
    childTable.addGlobal(1,"Joe")
    assert_equal(table._data[1], "Joe")
    assert("Joe" not in childTable._data.values())

