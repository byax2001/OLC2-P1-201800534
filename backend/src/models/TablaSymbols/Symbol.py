from models.TablaSymbols.Tipos import Tipos
from enum import Enum

class Symbols(Enum):
    VARIABLE=0
    ARREGLO=1
    FUNCION=2
    VECTOR=3

def getSymbol(s):
    if s==0:
        return Symbols.VARIABLE
    elif s==1:
        return Symbols.ARREGLO
    elif s==2:
        return Symbols.FUNCION
    elif s==3:
        return Symbols.VECTOR

    
class Symbol():
    def __init__(self,mut:bool,id: str, value, tipo_simbolo: int, tipo: Tipos,line:int,column:int) -> None:
        self.mut=mut
        self.id = id
        self.value = value
        self.tsimbolo = getSymbol(tipo_simbolo)  #Tipo de Variable: variable normal, arreglo, funcion
        self.tipo = tipo  #i64,f64, string, char
        self.line=line
        self.column=column
