from models.TablaSymbols.Tipos import Tipos

class ValC3d:
    def __init__(self,valor:str, isTemp:bool, tipo: Tipos) -> None:
        self.valor = valor
        self.isTemp = isTemp
        self.tipo = tipo
        self.trueLabel = ""
        self.falseLabel = ""

    def getValue(self) -> str:
        return self.valor