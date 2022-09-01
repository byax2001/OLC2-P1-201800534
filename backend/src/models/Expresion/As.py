from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import getTipo,Tipos,definirTipo
from models.TablaSymbols.Enviroment import Enviroment

class As(Expresion):
    def __init__(self, exp:Expresion,tipocast:str, line: int, column: int):
        self.value=None
        self.exp = exp
        self.tipo=getTipo(tipocast)
        self.line = line
        self.column = column
    def getValor(self, driver, ts):
        if self.exp.getTipo(driver,ts) in [Tipos.FLOAT64, Tipos.INT64]:
            valor=self.exp.getValor(driver,ts);
            if self.tipo==Tipos.INT64:
                return int(valor)
            elif self.tipo==Tipos.FLOAT64:
                return float(valor)
            elif self.tip==Tipos.USIZE:
                return abs(int(valor))
            else:
                print("Casteo \"as\" no valido ")
                return None
        else:
            print("Error, intento de casteo \"as\" para un valor no float o int ")
    def getTipo(self, driver, ts):
        tipo=definirTipo(self.getValor(driver, ts))
        if self.tipo==Tipos.USIZE:
            tipo=Tipos.USIZE
        return tipo