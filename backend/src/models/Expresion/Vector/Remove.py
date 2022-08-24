from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.Driver import Driver
from models.TablaSymbols.Symbol import Symbols
from models.TablaSymbols.Tipos import Tipos

class Remove(Expresion):
    def __init__(self, id: str, index: Expresion, line: int, column: int):
        self.value=None
        self.tipo=None
        self.id = id
        self.index = index
        self.line = line
        self.column = column


    def ejecutar(self, driver: Driver, ts: Enviroment):
        self.getValor(driver,ts);
    def getValor(self, driver, ts):
        if self.value==self.tipo==None:
            symbol = ts.buscar(self.id)
            v_index = self.index.getValor(driver, ts)
            t_index = self.index.getTipo(driver, ts)
            if symbol != None:  # si existe el vector, si ya fue declarado
                if symbol.mut == True:
                    if symbol.tsimbolo == Symbols.VECTOR:  # si lo que se llamo fue un vector
                        if t_index == Tipos.INT64:  # el index es un entero
                            vector = symbol.value
                            self.value=vector.remove(v_index)

                            if self.value!=None:
                                self.tipo=symbol.tipo
                            else:
                                self.tipo=Tipos.ERROR
                        else:
                            print(f"El index debe de ser un entero linea: {self.line}")
                    else:
                        print(f"Error Intento de Insert en una variable no vectorial  linea:{self.line} ")
                else:
                    print(f"Intento de Insert en vector no muteable linea: {self.line}")
            else:
                print(f"Error Intento de Insert en vector no declarado linea:{self.line} ")
        return self.value

    def getTipo(self, driver, ts):
        if self.value==self.tipo==None:
            self.getValor(driver,ts)
        return self.tipo