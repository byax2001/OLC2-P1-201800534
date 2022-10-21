from models.TablaSymbols.Tipos import Tipos
from enum import Enum
class Accesos(Enum):
    PUBLICO=0
    PRIVADO=1

class Symbols(Enum):
    VARIABLE=0
    ARREGLO=1
    FUNCION=2
    VECTOR=3
    OBJETO=4
    MOD=5

def getAcceso(s):
    if s==0:
        return Accesos.PUBLICO
    elif s==1:
        return Accesos.PRIVADO
    else:
        return Accesos.PUBLICO
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
        return Symbols.MOD
    
class Symbol():
    def __init__(self,mut:bool,id: str, value, tipo_simbolo: int, tipo: Tipos,line:int,column:int,tacceso:int=0,position:int=0) -> None:
        self.mut=mut
        self.id = id
        self.value = value
        self.tsimbolo = getSymbol(tipo_simbolo)  #Tipo de Variable: variable normal, arreglo, funcion
        self.tipo = tipo  #i64,f64, string, char
        self.line=line
        self.column=column
        self.tacceso = getAcceso(tacceso)
        self.position = position #esto es para hallar la posicion de esta variable en la pila
        self.func_create=False #para las funciones en c3d, evitando que se vuelvan a crear
        self.paso_parametro = False #por si declaro como paso de parametro
        self.tipo_return = self.tipo