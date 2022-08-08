from models.TablaSymbols.Tipos import Tipos
from enum import Enum

class Symbol(Enum):
    Variable=1

def getSymbol(s):
    if s==1:
        return Symbol.Variable
    
class Symbol():
    def __init__(self, simbolo: int, tipo: Tipos, id: str, value) -> None:
        self.value = value
        self.id = id
        self.tipo = tipo
        self.simbolo = getSymbol(simbolo)