from models.TablaSymbols.Tipos import Tipos
from enum import Enum
class Acceso(Enum):
    PUBLICO=0
    PRIVADO=1

class Symbols(Enum):
    VARIABLE=0
    ARREGLO=1
    FUNCION=2
    VECTOR=3
    OBJETO=4
    BASEDATOS=5

def getAcceso(s):
    if s==0:
        return Acceso.PUBLICO
    elif s==1:
        return Acceso.PRIVADO
    else:
        return Acceso.PUBLICO
def getSymbol(s):
    if s==0:
        return Symbols.VARIABLE
    elif s==1:
        return Symbols.ARREGLO
    elif s==2:
        return Symbols.FUNCION
    elif s==3:
        return Symbols.VECTOR
    elif s==4:
        return Symbols.OBJETO
    elif s==5:
        return Symbols.BASEDATOS
    
class Symbol():
    def __init__(self,mut:bool,id: str, value, tipo_simbolo: int, tipo: Tipos,line:int,column:int,tacceso:int=0) -> None:
        self.mut=mut
        self.id = id
        self.value = value
        self.tsimbolo = getSymbol(tipo_simbolo)  #Tipo de Variable: variable normal, arreglo, funcion
        self.tipo = tipo  #i64,f64, string, char
        self.line=line
        self.column=column
        self.tacceso = getAcceso(tacceso)
