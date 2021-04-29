
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "leftSUMARESTAleftMULTDIVMODDIV INTEGER MOD MULT RESTA SUMA\n        sentence : expr ';'\n        \n        sentence : empty ';'\n        \n        expr :   '(' expr ')'\n              | INTEGER\n        \n        expr : expr MULT expr\n              | expr DIV expr\n              | expr MOD expr\n        \n        expr :      expr SUMA expr\n                |   expr RESTA expr\n        empty :"
    
_lr_action_items = {'(':([0,4,7,8,9,10,11,],[4,4,4,4,4,4,4,]),'INTEGER':([0,4,7,8,9,10,11,],[5,5,5,5,5,5,5,]),';':([0,2,3,5,14,15,16,17,18,19,],[-10,6,12,-4,-5,-6,-7,-8,-9,-3,]),'$end':([1,6,12,],[0,-1,-2,]),'MULT':([2,5,13,14,15,16,17,18,19,],[7,-4,7,-5,-6,-7,7,7,-3,]),'DIV':([2,5,13,14,15,16,17,18,19,],[8,-4,8,-5,-6,-7,8,8,-3,]),'MOD':([2,5,13,14,15,16,17,18,19,],[9,-4,9,-5,-6,-7,9,9,-3,]),'SUMA':([2,5,13,14,15,16,17,18,19,],[10,-4,10,-5,-6,-7,-8,-9,-3,]),'RESTA':([2,5,13,14,15,16,17,18,19,],[11,-4,11,-5,-6,-7,-8,-9,-3,]),')':([5,13,14,15,16,17,18,19,],[-4,19,-5,-6,-7,-8,-9,-3,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'sentence':([0,],[1,]),'expr':([0,4,7,8,9,10,11,],[2,13,14,15,16,17,18,]),'empty':([0,],[3,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> sentence","S'",1,None,None,None),
  ('sentence -> expr ;','sentence',2,'p_sentencia','p3.py',44),
  ('sentence -> empty ;','sentence',2,'p_sentencia_buida','p3.py',53),
  ('expr -> ( expr )','expr',3,'p_expr','p3.py',59),
  ('expr -> INTEGER','expr',1,'p_expr','p3.py',60),
  ('expr -> expr MULT expr','expr',3,'p_expr_prioritat_alta','p3.py',75),
  ('expr -> expr DIV expr','expr',3,'p_expr_prioritat_alta','p3.py',76),
  ('expr -> expr MOD expr','expr',3,'p_expr_prioritat_alta','p3.py',77),
  ('expr -> expr SUMA expr','expr',3,'p_expr_prioritat_baixa','p3.py',84),
  ('expr -> expr RESTA expr','expr',3,'p_expr_prioritat_baixa','p3.py',85),
  ('empty -> <empty>','empty',0,'p_empty','p3.py',96),
]
