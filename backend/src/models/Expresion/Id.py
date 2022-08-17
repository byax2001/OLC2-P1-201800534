from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import definirTipo,Tipos
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
            symbol = ts.buscar(self.id);
            if symbol != None:
                self.tipo = symbol.tipo
            else:
                self.tipo =Tipos.ERROR
            return self.tipo
        else:
            return self.tipo

    def getValor(self, driver, ts:Enviroment):
        symbol = ts.buscar(self.id);
        if symbol!=None:
            self.value = symbol.value;
            return self.value
        else:
            return None
    def getSymbol(self,driver,ts:Enviroment):
        symbol = ts.buscar(self.id);
        if symbol != None:
            return symbol
        else:
            return None
    def ejecutar(self, driver, ts):
        """En la mayoria de expresiones no realiza nada"""
        pass