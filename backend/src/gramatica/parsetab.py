
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftmenosmasleftmultidivrightUNARIOand bool cadena caracter char coma cora corc decimal diferente div dospuntos entero f64 false i64 id igual igualigual interrogacion let llavea llavec mas mayor mayorigual menor menorigual menos mod multi mut not or para parc pow println puntoycoma str string struct true\n    INICIO : INSTRUCCIONES\n    \n    INSTRUCCIONES : INSTRUCCIONES INSTRUCCION\n    \n    INSTRUCCIONES : INSTRUCCION\n    \n    INSTRUCCION : PRINT puntoycoma\n        | DECLARACION puntoycoma\n    \n    EXPRESION : EXPRESION mas EXPRESION \n            |   EXPRESION menos EXPRESION\n            |   EXPRESION div EXPRESION\n            |   EXPRESION multi EXPRESION\n            |   EXPRESION mod EXPRESION  \n            |   pow para EXPRESION coma EXPRESION parc\n    \n    EXPRESION : menos EXPRESION %prec UNARIO\n    \n    EXPRESION :  EXPRESION mayor EXPRESION\n            |   EXPRESION menor EXPRESION\n            |   EXPRESION mayorigual EXPRESION\n            |   EXPRESION menorigual EXPRESION\n            |   EXPRESION igualigual EXPRESION\n            |   EXPRESION diferente EXPRESION\n    \n    EXPRESION :  EXPRESION and EXPRESION\n            |   EXPRESION or EXPRESION\n    \n    EXPRESION :  not EXPRESION\n    \n    EXPRESION : para EXPRESION parc\n    \n    EXPRESION : TIPODATO\n    \n    TIPODATO : entero\n        | decimal\n        | cadena\n        | caracter\n        | true\n        | false\n    \n    EXPRESION : id\n    \n    TIPOVAR : i64\n        | f64\n        | bool\n        | string\n        | char\n        | str\n    \n    PRINT : println para EXPRESION parc\n    \n    DECLARACION : let mut id dospuntos TIPOVAR igual EXPRESION\n                | let mut id igual EXPRESION\n    \n    DECLARACION : let id dospuntos TIPOVAR igual EXPRESION\n                | let id igual EXPRESION\n    \n    DECLARACION : let mut id dospuntos TIPOVAR\n    '
    
_lr_action_items = {'println':([0,2,3,8,9,10,],[6,6,-3,-2,-4,-5,]),'let':([0,2,3,8,9,10,],[7,7,-3,-2,-4,-5,]),'$end':([1,2,3,8,9,10,],[0,-1,-3,-2,-4,-5,]),'puntoycoma':([4,5,19,20,21,22,23,24,25,26,31,45,47,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,73,74,78,80,81,],[9,10,-23,-30,-24,-25,-26,-27,-28,-29,-37,-12,-21,-31,-32,-33,-34,-35,-36,-41,-22,-6,-7,-8,-9,-10,-13,-14,-15,-16,-17,-18,-19,-20,-42,-39,-40,-38,-11,]),'para':([6,11,14,16,17,18,29,32,33,34,35,36,37,38,39,40,41,42,43,44,46,49,75,76,77,],[11,14,14,14,46,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,]),'mut':([7,],[12,]),'id':([7,11,12,14,16,18,29,32,33,34,35,36,37,38,39,40,41,42,43,44,46,49,75,76,77,],[13,20,27,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,]),'pow':([11,14,16,18,29,32,33,34,35,36,37,38,39,40,41,42,43,44,46,49,75,76,77,],[17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,]),'menos':([11,14,15,16,18,19,20,21,22,23,24,25,26,29,30,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,49,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,74,75,76,77,78,79,80,81,],[16,16,33,16,16,-23,-30,-24,-25,-26,-27,-28,-29,16,33,16,16,16,16,16,16,16,16,16,16,16,16,16,-12,16,33,16,33,-22,-6,-7,-8,-9,33,33,33,33,33,33,33,33,33,33,33,16,16,16,33,33,33,-11,]),'not':([11,14,16,18,29,32,33,34,35,36,37,38,39,40,41,42,43,44,46,49,75,76,77,],[18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,]),'entero':([11,14,16,18,29,32,33,34,35,36,37,38,39,40,41,42,43,44,46,49,75,76,77,],[21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,]),'decimal':([11,14,16,18,29,32,33,34,35,36,37,38,39,40,41,42,43,44,46,49,75,76,77,],[22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,]),'cadena':([11,14,16,18,29,32,33,34,35,36,37,38,39,40,41,42,43,44,46,49,75,76,77,],[23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,]),'caracter':([11,14,16,18,29,32,33,34,35,36,37,38,39,40,41,42,43,44,46,49,75,76,77,],[24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,]),'true':([11,14,16,18,29,32,33,34,35,36,37,38,39,40,41,42,43,44,46,49,75,76,77,],[25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,]),'false':([11,14,16,18,29,32,33,34,35,36,37,38,39,40,41,42,43,44,46,49,75,76,77,],[26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,]),'dospuntos':([13,27,],[28,48,]),'igual':([13,27,50,51,52,53,54,55,56,73,],[29,49,75,-31,-32,-33,-34,-35,-36,77,]),'parc':([15,19,20,21,22,23,24,25,26,30,45,47,58,59,60,61,62,63,64,65,66,67,68,69,70,71,79,81,],[31,-23,-30,-24,-25,-26,-27,-28,-29,58,-12,-21,-22,-6,-7,-8,-9,-10,-13,-14,-15,-16,-17,-18,-19,-20,81,-11,]),'mas':([15,19,20,21,22,23,24,25,26,30,45,47,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,74,78,79,80,81,],[32,-23,-30,-24,-25,-26,-27,-28,-29,32,-12,32,32,-22,-6,-7,-8,-9,32,32,32,32,32,32,32,32,32,32,32,32,32,32,-11,]),'div':([15,19,20,21,22,23,24,25,26,30,45,47,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,74,78,79,80,81,],[34,-23,-30,-24,-25,-26,-27,-28,-29,34,-12,34,34,-22,34,34,-8,-9,34,34,34,34,34,34,34,34,34,34,34,34,34,34,-11,]),'multi':([15,19,20,21,22,23,24,25,26,30,45,47,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,74,78,79,80,81,],[35,-23,-30,-24,-25,-26,-27,-28,-29,35,-12,35,35,-22,35,35,-8,-9,35,35,35,35,35,35,35,35,35,35,35,35,35,35,-11,]),'mod':([15,19,20,21,22,23,24,25,26,30,45,47,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,74,78,79,80,81,],[36,-23,-30,-24,-25,-26,-27,-28,-29,36,-12,36,36,-22,-6,-7,-8,-9,36,36,36,36,36,36,36,36,36,36,36,36,36,36,-11,]),'mayor':([15,19,20,21,22,23,24,25,26,30,45,47,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,74,78,79,80,81,],[37,-23,-30,-24,-25,-26,-27,-28,-29,37,-12,37,37,-22,-6,-7,-8,-9,37,37,37,37,37,37,37,37,37,37,37,37,37,37,-11,]),'menor':([15,19,20,21,22,23,24,25,26,30,45,47,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,74,78,79,80,81,],[38,-23,-30,-24,-25,-26,-27,-28,-29,38,-12,38,38,-22,-6,-7,-8,-9,38,38,38,38,38,38,38,38,38,38,38,38,38,38,-11,]),'mayorigual':([15,19,20,21,22,23,24,25,26,30,45,47,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,74,78,79,80,81,],[39,-23,-30,-24,-25,-26,-27,-28,-29,39,-12,39,39,-22,-6,-7,-8,-9,39,39,39,39,39,39,39,39,39,39,39,39,39,39,-11,]),'menorigual':([15,19,20,21,22,23,24,25,26,30,45,47,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,74,78,79,80,81,],[40,-23,-30,-24,-25,-26,-27,-28,-29,40,-12,40,40,-22,-6,-7,-8,-9,40,40,40,40,40,40,40,40,40,40,40,40,40,40,-11,]),'igualigual':([15,19,20,21,22,23,24,25,26,30,45,47,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,74,78,79,80,81,],[41,-23,-30,-24,-25,-26,-27,-28,-29,41,-12,41,41,-22,-6,-7,-8,-9,41,41,41,41,41,41,41,41,41,41,41,41,41,41,-11,]),'diferente':([15,19,20,21,22,23,24,25,26,30,45,47,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,74,78,79,80,81,],[42,-23,-30,-24,-25,-26,-27,-28,-29,42,-12,42,42,-22,-6,-7,-8,-9,42,42,42,42,42,42,42,42,42,42,42,42,42,42,-11,]),'and':([15,19,20,21,22,23,24,25,26,30,45,47,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,74,78,79,80,81,],[43,-23,-30,-24,-25,-26,-27,-28,-29,43,-12,43,43,-22,-6,-7,-8,-9,43,43,43,43,43,43,43,43,43,43,43,43,43,43,-11,]),'or':([15,19,20,21,22,23,24,25,26,30,45,47,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,74,78,79,80,81,],[44,-23,-30,-24,-25,-26,-27,-28,-29,44,-12,44,44,-22,-6,-7,-8,-9,44,44,44,44,44,44,44,44,44,44,44,44,44,44,-11,]),'coma':([19,20,21,22,23,24,25,26,45,47,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,81,],[-23,-30,-24,-25,-26,-27,-28,-29,-12,-21,-22,-6,-7,-8,-9,-10,-13,-14,-15,-16,-17,-18,-19,-20,76,-11,]),'i64':([28,48,],[51,51,]),'f64':([28,48,],[52,52,]),'bool':([28,48,],[53,53,]),'string':([28,48,],[54,54,]),'char':([28,48,],[55,55,]),'str':([28,48,],[56,56,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'INICIO':([0,],[1,]),'INSTRUCCIONES':([0,],[2,]),'INSTRUCCION':([0,2,],[3,8,]),'PRINT':([0,2,],[4,4,]),'DECLARACION':([0,2,],[5,5,]),'EXPRESION':([11,14,16,18,29,32,33,34,35,36,37,38,39,40,41,42,43,44,46,49,75,76,77,],[15,30,45,47,57,59,60,61,62,63,64,65,66,67,68,69,70,71,72,74,78,79,80,]),'TIPODATO':([11,14,16,18,29,32,33,34,35,36,37,38,39,40,41,42,43,44,46,49,75,76,77,],[19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,]),'TIPOVAR':([28,48,],[50,73,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> INICIO","S'",1,None,None,None),
  ('INICIO -> INSTRUCCIONES','INICIO',1,'p_inicio','parser.py',34),
  ('INSTRUCCIONES -> INSTRUCCIONES INSTRUCCION','INSTRUCCIONES',2,'p_instrucciones_lista','parser.py',40),
  ('INSTRUCCIONES -> INSTRUCCION','INSTRUCCIONES',1,'p_instrucciones_instruccion','parser.py',46),
  ('INSTRUCCION -> PRINT puntoycoma','INSTRUCCION',2,'p_instruccion','parser.py',52),
  ('INSTRUCCION -> DECLARACION puntoycoma','INSTRUCCION',2,'p_instruccion','parser.py',53),
  ('EXPRESION -> EXPRESION mas EXPRESION','EXPRESION',3,'p_expresion_aritmeticas','parser.py',59),
  ('EXPRESION -> EXPRESION menos EXPRESION','EXPRESION',3,'p_expresion_aritmeticas','parser.py',60),
  ('EXPRESION -> EXPRESION div EXPRESION','EXPRESION',3,'p_expresion_aritmeticas','parser.py',61),
  ('EXPRESION -> EXPRESION multi EXPRESION','EXPRESION',3,'p_expresion_aritmeticas','parser.py',62),
  ('EXPRESION -> EXPRESION mod EXPRESION','EXPRESION',3,'p_expresion_aritmeticas','parser.py',63),
  ('EXPRESION -> pow para EXPRESION coma EXPRESION parc','EXPRESION',6,'p_expresion_aritmeticas','parser.py',64),
  ('EXPRESION -> menos EXPRESION','EXPRESION',2,'p_factor_unario','parser.py',78),
  ('EXPRESION -> EXPRESION mayor EXPRESION','EXPRESION',3,'p_expresion_relacionales','parser.py',84),
  ('EXPRESION -> EXPRESION menor EXPRESION','EXPRESION',3,'p_expresion_relacionales','parser.py',85),
  ('EXPRESION -> EXPRESION mayorigual EXPRESION','EXPRESION',3,'p_expresion_relacionales','parser.py',86),
  ('EXPRESION -> EXPRESION menorigual EXPRESION','EXPRESION',3,'p_expresion_relacionales','parser.py',87),
  ('EXPRESION -> EXPRESION igualigual EXPRESION','EXPRESION',3,'p_expresion_relacionales','parser.py',88),
  ('EXPRESION -> EXPRESION diferente EXPRESION','EXPRESION',3,'p_expresion_relacionales','parser.py',89),
  ('EXPRESION -> EXPRESION and EXPRESION','EXPRESION',3,'p_expresion_logicas','parser.py',95),
  ('EXPRESION -> EXPRESION or EXPRESION','EXPRESION',3,'p_expresion_logicas','parser.py',96),
  ('EXPRESION -> not EXPRESION','EXPRESION',2,'p_expresion_logicas_not','parser.py',101),
  ('EXPRESION -> para EXPRESION parc','EXPRESION',3,'p_EXPRESION_par','parser.py',107),
  ('EXPRESION -> TIPODATO','EXPRESION',1,'p_exp_tdato','parser.py',113),
  ('TIPODATO -> entero','TIPODATO',1,'p_tipo_dato','parser.py',119),
  ('TIPODATO -> decimal','TIPODATO',1,'p_tipo_dato','parser.py',120),
  ('TIPODATO -> cadena','TIPODATO',1,'p_tipo_dato','parser.py',121),
  ('TIPODATO -> caracter','TIPODATO',1,'p_tipo_dato','parser.py',122),
  ('TIPODATO -> true','TIPODATO',1,'p_tipo_dato','parser.py',123),
  ('TIPODATO -> false','TIPODATO',1,'p_tipo_dato','parser.py',124),
  ('EXPRESION -> id','EXPRESION',1,'p_id','parser.py',129),
  ('TIPOVAR -> i64','TIPOVAR',1,'p_tipo_var','parser.py',134),
  ('TIPOVAR -> f64','TIPOVAR',1,'p_tipo_var','parser.py',135),
  ('TIPOVAR -> bool','TIPOVAR',1,'p_tipo_var','parser.py',136),
  ('TIPOVAR -> string','TIPOVAR',1,'p_tipo_var','parser.py',137),
  ('TIPOVAR -> char','TIPOVAR',1,'p_tipo_var','parser.py',138),
  ('TIPOVAR -> str','TIPOVAR',1,'p_tipo_var','parser.py',139),
  ('PRINT -> println para EXPRESION parc','PRINT',4,'p_println','parser.py',146),
  ('DECLARACION -> let mut id dospuntos TIPOVAR igual EXPRESION','DECLARACION',7,'p_declaracion_t1','parser.py',152),
  ('DECLARACION -> let mut id igual EXPRESION','DECLARACION',5,'p_declaracion_t1','parser.py',153),
  ('DECLARACION -> let id dospuntos TIPOVAR igual EXPRESION','DECLARACION',6,'p_declaracion_t2','parser.py',163),
  ('DECLARACION -> let id igual EXPRESION','DECLARACION',4,'p_declaracion_t2','parser.py',164),
  ('DECLARACION -> let mut id dospuntos TIPOVAR','DECLARACION',5,'p_declaracion_t3','parser.py',173),
]
