from enum import Enum

class Tipos(Enum):
    INT64 = 1
    FLOAT64 = 2
    STRING = 3
    STR = 4
    CHAR = 5
    BOOLEAN = 6
    ERROR = 7
    ID = 8
    VOID = 9
    USIZE=10 #int pero siempre mayor que 0
    STRUCT=11


def getTipo(s:str):
    if s=="i64":
        return Tipos.INT64
    elif s=="f64":
        return Tipos.FLOAT64
    elif s=="bool":
        return Tipos.BOOLEAN
    elif s=="char":
        return Tipos.CHAR
    elif s=="String":
        return Tipos.STRING
    elif s=="&str":
        return Tipos.STR
    elif s=="usize":
        return Tipos.USIZE
    elif  s!="" and len(s)>0:  ## no es "" significa que es un id por tanto es un struct
        return Tipos.STRUCT
    else:
        return Tipos.ERROR

def definirTipo(value):

    if type(value) == float:
        return Tipos.FLOAT64
    elif type(value) == int:
        return Tipos.INT64
    elif type(value) == str:
        return Tipos.STR
    elif type(value) == bool:
        return Tipos.BOOLEAN
    else:
        return Tipos.ERROR

    
class Tipo:
    def __init__(self, stipo: str):
        self.stipo = stipo
        self.tipo = getTipo(stipo)

    def getSTipo(self):
        return self.stipo

