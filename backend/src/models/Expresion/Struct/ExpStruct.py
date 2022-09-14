from models.Abstract.Expresion import Expresion


class ExpStruct(Expresion):
    def __init__(self,id:str,exp1:Expresion,line:int,column:int):
        self.id=id
        self.exp=exp1
        self.tipo=line
        self.column=column