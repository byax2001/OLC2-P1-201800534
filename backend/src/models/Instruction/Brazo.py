from models.Abstract.Instruction import Instruccion
from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.ValC3d import ValC3d


class Brazo(Instruccion):
    def __init__(self,cExp:[Expresion],bloque:[Instruccion],line:int,column:int):
        super().__init__()
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

    def generarC3d(self,ts,ptr:int):
        new_ts = Enviroment(ts, 'Brazo Match')
        for instruccion in self.bloque:
            instruccion.generator=self.generator
            instruccion.generarC3d(new_ts,ptr)

    def CmpExpB(self,expM:ValC3d,Lainst,ts,ptr):
        for exp in self.cExp:
            _exp:ValC3d = exp.generarC3d(ts,ptr)
            self.generator.addIf(left=expM.valor,rigth=_exp.valor,operator="==",label=Lainst)