from models.Instruction.Instruction import Instruccion
from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.Tipos import Tipos,definirTipo

class Brazo(Instruccion):
    def __init__(self,exp:Expresion,bloque:[Instruccion],line:int,column:int):
        self.exp=exp
        self.bloque=bloque
        self.line=line
        self.column=column
    def ejecutar(self, driver, ts: Enviroment):
        #Crear un nuevo enviroment
        new_ts = Enviroment(ts, 'Brazo Match')
        for instruccion in self.bloque:
            instruccion.ejecutar(driver,new_ts)

    def getV_ExpBrazo(self, driver, ts: Enviroment):
        value = self.exp.getValor(driver,ts)
        return value
    def getT_ExpBrazo(self,driver,ts:Enviroment):
        tipo = definirTipo(self.getV_ExpBrazo(driver,ts));
        return tipo