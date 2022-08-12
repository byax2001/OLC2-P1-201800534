from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import definirTipo
from models.TablaSymbols.Enviroment import Enviroment

class Id(Expresion):    
    def __init__(self, id:str, linea: int, columna: int):
        self.tipo=None
        self.value=None
        self.id = id
        self.linea = linea
        self.columna = columna

    def getTipo(self, driver, ts):
        if self.tipo is None or self.value is None:
            self.value = self.getValor(driver, ts)
            self.tipo = definirTipo(self.value)
            return self.tipo
        else:
            return self.tipo

    def getValor(self, driver, ts:Enviroment):
        symbol = ts.buscar(self.id);
        if symbol!=None:
            self.value = symbol.value;
            self.tipo = definirTipo(self.value)
            return self.value
        else:
            return None