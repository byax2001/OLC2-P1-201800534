from enum import Enum
from models.Abstract.Expresion import Expresion


class OperadorLog(Enum):
    OR=1
    AND=2
    NOT=3


def getOperador(op) -> OperadorLog:
    if op == '||':
        return OperadorLog.OR
    elif op == '&&':
        return OperadorLog.AND
    elif op == '!':
        return OperadorLog.NOT

class OperacionLog(Expresion):
    def __init__(self, exp1: Expresion, operador, exp2: Expresion, expU, linea, columna):
        super().__init__()
        self.expU = expU
        self.columna = columna
        self.linea = linea
        self.exp2 = exp2
        self.operador = getOperador(operador)
        self.exp1 = exp1
        self.value=None
        self.tipo=None
        self.instancia=0