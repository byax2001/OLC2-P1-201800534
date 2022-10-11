from models.TablaSymbols.Tipos import Tipos

class ValC3d:
    def __init__(self,valor:str, isTemp:bool, tipo: Tipos,tipo_aux:Tipos=Tipos.ERROR) -> None:
        self.valor = valor
        self.isTemp = isTemp
        self.tipo = tipo
        self.tipo_aux = tipo_aux  #para identificar si es un arreglo o no
        self.prof_array=0 #profundidad de un arreglo
        self.trueLabel = ""
        self.falseLabel = ""

    def getValue(self) -> str:
        return self.valor