from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Types import definirTipo,Types


class Id(Expresion):    
    def __init__(self, valor, linea: int, columna: int):
        self.tipo = None
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def getTipo(self, driver, ts):
        if self.tipo is None:
            value = self.getValor(driver, ts)
            return definirTipo(value)
        else:
            return self.tipo

    def getValor(self, driver, ts):
        #metodo para obtener un valor que esta adentro de una tabla de datos 
        value = self.valor
        self.tipo = definirTipo(value)
        return value