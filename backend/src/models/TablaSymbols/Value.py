from models.TablaSymbols.Tipos import Tipos

class Value:
    def __init__(self,valor, isTemp:bool, tipo: Tipos) -> None:
        self.value = valor
        self.isTemp = isTemp
        self.tipo = tipo
        self.trueLabel = ""
        self.falseLabel = ""

    def getValue(self) -> str:
        return self.value