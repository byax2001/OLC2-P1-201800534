from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.Driver import Driver
from models.TablaSymbols.Symbol import Symbols
from models.TablaSymbols.Tipos import Tipos,definirTipo

class AccesVec(Expresion):
    def __init__(self, id: str,cIndex:[Expresion], line: int, column: int):
        self.value=None
        self.tipo=None
        self.id = id
        self.cIndex=cIndex
        self.line = line
        self.column = column

    def ejecutar(self,driver,ts):
        pass
    def getValor(self, driver, ts):
        if self.value == self.tipo == None:
            symbol = ts.buscar(self.id)
            vecIndex=[]
            for index in self.cIndex:
                if index[0].getTipo(driver,ts)==Tipos.INT64:  #cIndex= [[expresion],[expresion],[expresion]]
                    vecIndex.append(index.getValor(driver,ts))
                else:
                    print(f"Error: uno de los index no es un entero {self.line}")
                    return
            if symbol != None:  # si existe el vector, si ya fue declarado
                if symbol.tsimbolo == Symbols.VECTOR or symbol.tsimbolo==Symbols.ARREGLO:  # si lo que se llamo fue un vector o arreglo
                    vector = symbol.value
                    self.value = vector.acces(vecIndex)
                    if self.value != None:
                        self.tipo = symbol.tipo
                    else:
                        self.tipo = Tipos.ERROR
                else:
                    print(f"Error Intento de obtener valor en una variable no vectorial  linea:{self.line} ")
            else:
                print(f"Error Intento de Insert en vector no declarado linea:{self.line} ")
    def getTipo(self, driver, ts):
        if self.value==None:
            self.getValor(driver,ts)
            if self.value==None: #si despues de eso aun es None entonces da error al intentar obtener un valor
                self.tipo==Tipos.ERROR
        return self.tipo