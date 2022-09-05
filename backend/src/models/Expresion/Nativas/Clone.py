from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos,definirTipo
from BaseDatos.B_datos import B_datos
class Clone(Expresion):
    def __init__(self,exp:Expresion,line:int,column:int):
        self.exp=exp
        self.line=line
        self.column=column
    def getValor(self, driver, ts):
        return self.exp.getValor(driver,ts)
    def getTipo(self, driver, ts):
        return self.exp.getTipo(driver,ts)
        # o solo simplemente return Tipos.STRING
    def ejecutar(self,driver,ts):
        pass