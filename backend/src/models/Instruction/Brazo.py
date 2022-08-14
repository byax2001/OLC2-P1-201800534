from models.Instruction.Instruction import Instruccion
from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.Tipos import Tipos,definirTipo

class Brazo(Instruccion):
    def __init__(self,cExp:[Expresion],bloque:[Instruccion],line:int,column:int):
        self.cExp=cExp
        self.bloque=bloque
        self.line=line
        self.column=column
    def ejecutar(self, driver, ts: Enviroment):
        #Crear un nuevo enviroment
        new_ts = Enviroment(ts, 'Brazo Match')
        for instruccion in self.bloque:
            instruccion.ejecutar(driver,new_ts)
    def CompararVexps(self,driver,ts,valorEmatch):
        for exp in self.cExp:
            if exp.getValor(driver, ts)==valorEmatch:
                return True
        return False

    def CompararTexps(self,driver,ts:Enviroment,tipoEMatch):
        for element in self.cExp:
            if element.getTipo(driver,ts) !=tipoEMatch:
                return False
        return True