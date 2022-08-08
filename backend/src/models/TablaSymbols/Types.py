from enum import Enum

class Types(Enum):
    INT64 = 1
    FLOAT64 = 2
    STRING = 3
    CHAR = 4
    BOOLEAN=5
    ERROR=6
    ID=7
    
def getTipo(s:str):
    if s=="i64":
        return Types.INT64
    elif s=="f64":
        return Types.FLOAT64
    elif s=="bool":
        return Types.BOOLEAN
    elif s=="char":
        return Types.CHAR
    elif s=="&str" or s=="String":
        return Types.STRING

def definirTipo(value):
    if type(value) == float:
        return Types.FLOAT64
    elif type(value) == int:
        return Types.INT64
    elif type(value) == str:
        return Types.STRING
    elif type(value) == bool:
        return Types.BOOLEAN
    else:
        return None
    
class Types:
    def __init__(self, stipo: str):
        self.stipo = stipo
        self.tipo = getTipo(stipo)

    def getSTipo(self):
        return self.stipo

