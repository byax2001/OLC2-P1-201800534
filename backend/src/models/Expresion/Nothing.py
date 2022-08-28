from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
class Nothing(Expresion):
    def __init__(self,line,column):
        self.line=line
        self.column=column
    def getValor(self, driver, ts):
        return None
    def getTipo(self, driver, ts):
        return Tipos.ERROR
    def ejecutar(self,driver,ts):
        pass