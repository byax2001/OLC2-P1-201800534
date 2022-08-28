from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos,getTipo

class ExpStruct(Expresion):
    def __init__(self,id:str,exp1:Expresion,line:int,column:int):
        self.id=id
        self.exp=exp1
        self.tipo=line
        self.column=column