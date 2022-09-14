from models.Abstract.Instruction import Instruccion
from models.TablaSymbols.Enviroment import Enviroment
from models.Abstract import Expresion
from models import Driver

class Return(Instruccion):
    def __init__(self, exp: Expresion, line:int, column:int):
        self.exp=exp
        self.line = line
        self.column = column
    def ejecutar(self, driver: Driver, ts: Enviroment):
        if self.exp==None:
            return None
        else:
            return self.exp
