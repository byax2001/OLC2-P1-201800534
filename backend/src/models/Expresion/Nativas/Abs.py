from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos

class Abs(Expresion):
    def __init__(self,exp:Expresion,line:int,column:int):
        self.exp=exp
        self.line=line
        self.column=column
    def getValor(self, driver, ts):
        #ABS NO FUNCIONA SI LA EXPRESION QUE SE INTENTA ANALIZAR NO ES UN ID
        if self.exp.getTipo(driver,ts) in [Tipos.FLOAT64,Tipos.INT64]:
            return abs(self.exp.getValor(driver,ts))
        else:
            print("Error se esta intentando hacer abs a un dato no numerico")
    def getTipo(self, driver, ts):
        if self.exp.getTipo(driver, ts) in [Tipos.FLOAT64, Tipos.INT64]:
            return self.exp.getTipo(driver,ts)
        else:
            return Tipos.ERROR