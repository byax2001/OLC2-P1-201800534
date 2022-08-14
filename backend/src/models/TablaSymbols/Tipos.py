from enum import Enum

class Tipos(Enum):
    INT64 = 1
    FLOAT64 = 2
    STRING = 3
    CHAR = 4
    BOOLEAN = 5
    ERROR = 6
    ID = 7

def getTipo(s:str):
    if s=="i64":
        return Tipos.INT64
    elif s=="f64":
        return Tipos.FLOAT64
    elif s=="bool":
        return Tipos.BOOLEAN
    elif s=="char":
        return Tipos.CHAR
    elif s=="&str" or s=="String":
        return Tipos.STRING
    else:
        return None

def definirTipo(value):

    if type(value) == float:
        return Tipos.FLOAT64
    elif type(value) == int:
        return Tipos.INT64
    elif type(value) == str:
        return Tipos.STRING
    elif type(value) == bool:
        return Tipos.BOOLEAN
    else:
        return None

    
class Tipo:
    def __init__(self, stipo: str):
        self.stipo = stipo
        self.tipo = getTipo(stipo)

    def getSTipo(self):
        return self.stipo

