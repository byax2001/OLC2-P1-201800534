from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
import math
class Sqrt(Expresion):
    def __init__(self,exp:Expresion,line:int,column:int):
        self.exp=exp
        self.line=line
        self.column=column
    def getValor(self, driver, ts):
        if self.exp.getTipo(driver,ts) == Tipos.FLOAT64:
            return math.sqrt(self.exp.getValor(driver,ts))
        elif self.exp.getTipo(driver,ts) == Tipos.INT64:
            return math.trunc(math.sqrt(self.exp.getValor(driver, ts)))
        else:
            print("Error se esta intentando hacer sqrt a un dato no numerico")
    def getTipo(self, driver, ts):
        if self.exp.getTipo(driver, ts) in [Tipos.FLOAT64, Tipos.INT64]:
            return self.exp.getTipo(driver,ts)
        else:
            return Tipos.ERROR