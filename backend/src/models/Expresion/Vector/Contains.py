from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.Driver import Driver
from models.TablaSymbols.Symbol import Symbols
from models.TablaSymbols.Tipos import Tipos,definirTipo

class Contains(Expresion):
    def __init__(self, id: str, exp: Expresion, line: int, column: int):
        self.value=None
        self.tipo=None
        self.id = id
        self.index = exp
        self.line = line
        self.column = column


    def ejecutar(self, driver: Driver, ts: Enviroment):
        self.getValor(driver,ts);
    def getValor(self, driver, ts):
        if self.value==self.tipo==None:
            symbol = ts.buscar(self.id)
            v_exp = self.index.getValor(driver, ts)
            t_exp = self.index.getTipo(driver, ts)
            if symbol != None:  # si existe el vector, si ya fue declarado
                if symbol.tsimbolo == Symbols.VECTOR or symbol.tsimbolo==Symbols.ARREGLO:  # si lo que se llamo fue un vector o arreglo
                    if t_exp != Tipos.ERROR and v_exp != None:
                        vector = symbol.value
                        self.value = vector.contains(v_exp)
                    else:
                        print(f"La expresion a analizar da error: {self.line}")
                else:
                    print(f"Error Intento de Contain en una variable no vectorial o Arreglo  linea:{self.line} ")
            else:
                print(f"Error Contain en vector o Arreglo no declarado linea:{self.line} ")
        return self.value

    def getTipo(self, driver, ts):
        if self.value==None:
            self.tipo=definirTipo(self.getValor(driver,ts))
        return self.tipo