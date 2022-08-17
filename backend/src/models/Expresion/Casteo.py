from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import definirTipo,Tipos
from models.TablaSymbols.Enviroment import Enviroment

class Casteo(Expresion):
    def __init__(self, exp:Expresion,tipocast:str, linea: int, columna: int):
        self.tipo=None
        self.value=None
        self.id = exp
        self.tipocast=tipocast
        self.linea = linea
        self.columna = columna
    def getValor(self, driver, ts):
        print()
    def getTipo(self, driver, ts):
        print()