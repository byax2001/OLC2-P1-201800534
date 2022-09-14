from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.Driver import Driver
from models.TablaSymbols.Symbol import Symbols
from models.TablaSymbols.Tipos import definirTipo
from BaseDatos.B_datos import B_datos
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
                error = "Error Intento de Contain en una variable no vectorial  "
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        else:
            print(f"Error Contain en vector no declarado linea:{self.line} ")
            error = "Error Contain en vector no declarado"
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
        return self.value

    def getTipo(self, driver, ts):
        self.tipo=definirTipo(self.getValor(driver,ts))
        return self.tipo