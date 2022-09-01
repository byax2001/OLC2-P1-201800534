from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.Driver import Driver
from models.TablaSymbols.Symbol import Symbols
from models.TablaSymbols.Tipos import Tipos,definirTipo

class Capacity(Expresion):
    def __init__(self, id: str, line: int, column: int):
        self.value=None
        self.tipo=None
        self.id = id
        self.line = line
        self.column = column


    def ejecutar(self, driver: Driver, ts: Enviroment):
        pass
    def getValor(self, driver, ts):
        symbol = ts.buscar(self.id)
        if symbol != None:  # si existe el vector, si ya fue declarado
            if symbol.tsimbolo == Symbols.VECTOR:  # si lo que se llamo fue un vector
                vector = symbol.value
                self.value = vector.rcapacity()
            else:
                print(f"Error Intento de Contain en una variable no vectorial  linea:{self.line} ")
        else:
            print(f"Error Contain en vector no declarado linea:{self.line} ")
        return self.value

    def getTipo(self, driver, ts):
        self.tipo=definirTipo(self.getValor(driver,ts))
        return self.tipo