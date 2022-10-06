from models.Abstract.Instruction import Instruccion
from models.TablaSymbols.Enviroment import Enviroment
from models.Abstract import Expresion
from models import Driver
from models.TablaSymbols.ValC3d import ValC3d
from models.TablaSymbols.Tipos import Tipos

class Break(Instruccion):
    def __init__(self, exp: Expresion, line:int, column:int):
        super().__init__()
        self.exp = exp
        self.linea = line
        self.columna = column
    def ejecutar(self, driver: Driver, ts: Enviroment):
        pass
    def getValor(self,driver,ts):
        return self.exp.getValor(driver,ts);
    def getTipo (self,driver,ts):
        return self.exp.getTipo(driver,ts)
    def generarC3d(self,ts,ptr:int):
        self.generator.addCode("break_i")
        result=ValC3d(valor="0",isTemp=False,tipo=Tipos.ERROR,tipo_aux=Tipos.ERROR)
        if self.exp!=None:
            self.exp.generator=self.generator
            result=self.exp.generarC3d(ts,ptr)
        return result