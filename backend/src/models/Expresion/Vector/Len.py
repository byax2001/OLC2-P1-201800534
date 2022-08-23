from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.Driver import Driver
from models.TablaSymbols.Symbol import Symbols
from models.TablaSymbols.Tipos import Tipos,definirTipo

class Len(Expresion):
    def __init__(self,id:str,line:int,column:int):
        self.id=id
        self.value=None
        self.tipo=None
        self.line=line
        self.column=column

    def ejecutar(self,driver,ts):
        pass
    def getValor(self, driver, ts):
        if self.value == self.tipo == None:
            symbol = ts.buscar(self.id)
            if symbol != None:  # si existe el vector, si ya fue declarado
                if symbol.tsimbolo == Symbols.VECTOR or symbol.tsimbolo==Symbols.ARREGLO:  # si lo que se llamo fue un vector o arreglo
                    vector = symbol.value
                    self.value = vector.len()
                else:
                    print(f"Error Intento de uso de Len en una variable no vectorial o Arreglo linea:{self.line} ")
            else:
                print(f"Error Len en vector o Arreglo no declarado linea:{self.line} ")
        return self.value
    def getTipo(self, driver, ts):
        self.tipo=definirTipo(self.getValor(driver,ts))
        return self.tipo