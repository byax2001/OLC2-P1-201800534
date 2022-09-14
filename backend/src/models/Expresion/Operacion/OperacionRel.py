from enum import Enum
from models.Abstract.Expresion import Expresion


class OperadorRel(Enum):
    MAYORQUE=1
    MENORQUE=2
    MAYORIGUALQUE=3
    MENORIGUALQUE=4
    IGUALQUE=5
    DIFERENTEQUE=6


def getOperador(op) -> OperadorRel:
    if op == '>':
        return OperadorRel.MAYORQUE
    elif op == '<':
        return OperadorRel.MENORQUE
    elif op == '>=':
        return OperadorRel.MAYORIGUALQUE
    elif op == '<=':
        return OperadorRel.MENORIGUALQUE
    elif op == '==':
        return OperadorRel.IGUALQUE
    elif op == "!=":
        return OperadorRel.DIFERENTEQUE

class OperacionRel(Expresion):
    def __init__(self, exp1: Expresion, operador, exp2: Expresion, linea, columna):
        super().__init__()
        self.columna = columna
        self.linea = linea
        self.exp2 = exp2
        self.operador = getOperador(operador)
        self.exp1 = exp1
        self.tipo=None
        self.value=None
        self.instancia=0