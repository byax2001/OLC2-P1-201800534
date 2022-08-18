from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos,definirTipo

class ToStringOwned(Expresion):
    def __init__(self,exp:Expresion,line:int,column:int):
        self.exp=exp
        self.line=line
        self.column=column
    def getValor(self, driver, ts):
        return str(self.exp.getValor(driver,ts))
    def getTipo(self, driver, ts):
        return Tipos.STRING
        # o solo simplemente return Tipos.STRING