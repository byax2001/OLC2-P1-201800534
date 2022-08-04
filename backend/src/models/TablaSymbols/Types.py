from enum import Enum

class Types(Enum):
    INT64 = 1
    FLOAT64 = 2
def getTipo(s:str):
    if s=="INT64":
        return Types.INT64
    elif s=="FLOAT64":
        return Types.FLOAT64

def definirTipo(value):
    if type(value) == float:
        return Types.FLOAT64
    elif type(value) == int:
        return Types.INT64
    else:
        return None
class Types:
    def __init__(self, stipo: str):
        self.stipo = stipo
        self.tipo = getTipo(stipo)

    def getSTipo(self):
        return self.stipo

