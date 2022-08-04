from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Types import definirTipo


class Primitivo(Expresion):

    def __init__(self, v_primitivo, linea: int, columna: int):
        self.tipo = None
        self.v_primitivo = v_primitivo
        self.linea = linea
        self.columna = columna

    def getTipo(self, driver, ts):
        if self.tipo is None:
            value = self.getValor(driver, ts)
            return definirTipo(value)
        else:
            return self.tipo

    def getValor(self, driver, ts):
        value = self.v_primitivo
        self.tipo = definirTipo(value)
        return value