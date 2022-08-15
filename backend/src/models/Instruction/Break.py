from models.Instruction.Instruction import Instruccion
from models.TablaSymbols.Enviroment import Enviroment
from models.Expresion import Expresion
from models import Driver

class Break(Instruccion):
    def __init__(self,exp:Expresion,line:int, column:int):
        self.exp = exp
        self.linea = line
        self.columna = column
    def ejecutar(self, driver: Driver, ts: Enviroment):
        pass
    def getValor(self,driver,ts):
        return self.exp.getValor(driver,ts);
    def getTipo (self,driver,ts):
        return self.exp.getTipo(driver,ts)