from enum import Enum
from models.Abstract.Expresion import Expresion


class Operador(Enum):
    SUMA = 1
    RESTA = 2
    MULTI = 3
    DIV = 4
    UNARIO = 5
    MOD = 6
    POW = 7
    POWF = 8



def getOperador(op) -> Operador:
    if op == '+':
        return Operador.SUMA
    elif op == '-':
        return Operador.RESTA
    elif op == '*':
        return Operador.MULTI
    elif op == '/':
        return Operador.DIV
    elif op == 'UNARIO':
        return Operador.UNARIO
    elif op == "%":
        return Operador.MOD
    elif op == 'pow':
        return Operador.POW
    elif op == 'powf':
        return Operador.POWF


#lambda es una minifuncion que solo necesita de un par de parametros, no se uso en esta ocasion
def getOperacion(op: Operador):
    if op == Operador.SUMA:
        return lambda num1, num2: num1 + num2
    elif op == Operador.RESTA:
        return lambda num1, num2: num1 - num2
    elif op == Operador.MULTI:
        return lambda num1, num2: num1 * num2
    elif op == Operador.DIV:
        return lambda num1, num2: num1 / num2


class Operacion(Expresion):
    def __init__(self, exp1: Expresion, operador, exp2: Expresion, expU, linea, columna):
        super().__init__()
        self.value=None
        self.tipo=None
        self.expU = expU
        self.columna = columna
        self.linea = linea
        self.exp2 = exp2
        self.operador = getOperador(operador)
        self.exp1 = exp1
        self.instancia=0