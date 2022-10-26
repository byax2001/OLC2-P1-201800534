from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
class Nothing(Expresion):
    def __init__(self,line,column):
        super().__init__()
        self.line=line
        self.column=column
    def getValor(self, driver, ts):
        return None
    def getTipo(self, driver, ts):
        return Tipos.ERROR
    def ejecutar(self,driver,ts):
        pass
    def generarC3d(self,ts,ptr):
        pass