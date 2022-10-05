from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.ValC3d import ValC3d
from models.TablaSymbols.Tipos import Tipos

class BrazoTer(Expresion):
    #brazo :  EXPRESION | EXPRESION | EXPRESION : BLOQUE  / EXPRESION : BLOQUE
    def __init__(self,cExp:[Expresion],bloque:Expresion, line: int, column: int):
        super().__init__()
        self.tipo=None
        self.value=None
        self.cExp=cExp
        self.bloque=bloque
        self.linea = line
        self.columna = column
    def getValor(self, driver, ts):
        #if self.value is None:
        self.value= self.bloque.getValor(driver, ts)
        return self.value
    def getTipo(self, driver, ts):
        #if self.tipo is None:
        self.tipo = self.bloque.getTipo(driver,ts)
        return self.tipo

    def CompararVexps(self, driver, ts, valorEmatch):
        for exp in self.cExp:
            if exp.getValor(driver, ts) == valorEmatch: #si coincide con alguna empezar inmediatamente a ejecutar su bloque
                return True
        return False

    def CompararTexps(self, driver, ts: Enviroment, tipoEMatch):
        for element in self.cExp:
            if element.getTipo(driver, ts) != tipoEMatch:
                return False
        return True

    def ejecutar(self, driver, ts):
        """En la mayoria de expresiones no realiza nada"""
        pass
    def generarC3d(self,ts,ptr:int,tmpF):
        new_ts = Enviroment(ts, 'Brazo Match')
        self.bloque.generator.generator=self.generator
        result:ValC3d=self.bloque.generarC3d(new_ts,ptr)
        if result.tipo!=Tipos.BOOLEAN:
            self.generator.addExpAsign(target=tmpF,right=result.valor)
        return result


    def CmpExpB(self, expM: ValC3d, Lainst, ts, ptr):
        for exp in self.cExp:
            _exp: ValC3d = exp.generarC3d(ts, ptr)
            self.generator.addIf(left=expM.valor, rigth=_exp.valor, operator="==", label=Lainst)