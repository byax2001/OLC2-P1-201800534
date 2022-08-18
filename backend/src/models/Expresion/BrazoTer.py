from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import definirTipo,Tipos
from models.TablaSymbols.Enviroment import Enviroment
class BrazoTer(Expresion):
    #brazo :  EXPRESION | EXPRESION | EXPRESION : BLOQUE  / EXPRESION : BLOQUE
    def __init__(self,cExp:[Expresion],bloque:Expresion, line: int, column: int):
        self.tipo=None
        self.value=None
        self.cExp=cExp
        self.bloque=bloque
        self.linea = line
        self.columna = column
    def getValor(self, driver, ts):
        if self.value is None:
            self.value= self.bloque.getValor(driver, ts)
        return self.value
    def getTipo(self, driver, ts):
        if self.tipo is None:
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