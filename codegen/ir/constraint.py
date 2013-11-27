from ir_node import IRNode

class Constraint(IRNode):
  EQ = '='
  NEQ = '<>'
  GT = '>'
  GTE = '>='
  LT = '<'
  LTE = '<='
  IS = 'IS'
  ISNOT = 'IS NOT'
  NULL = 'NULL'
  NOT = 'NOT'

  constraint_map = {  '='       :     'EQ',  
                      '<>'      :    'NEQ', 
                      '>'       :     'GT',  
                      '>='      :    'GTE', 
                      '<'       :    'LT',   
                      '<='      :    'LTE', 
                      'IS'      :     'IS',  
                      'IS NOT'  :  'ISNOT', 
                      'NULL'    :   'NULL', 
                      'NOT'     :    'NOT'} 


  def __init__(self, op, left, right):
    self._op = op
    self._left = left
    self._right = right

  def getOp(self):
    return self._op

  def getLeftTerm(self):
    return self._left

  def getRightTerm(self):
    return self._right


  def __repr__(self):
    return self.constraint_map[self.getOp()] + '(' + str(self.getLeftTerm()) + ',' + str(self.getRightTerm()) + ')'
