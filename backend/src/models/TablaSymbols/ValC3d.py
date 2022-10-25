from models.TablaSymbols.Tipos import Tipos

class ValC3d:
    def __init__(self,valor:str, isTemp:bool, tipo: Tipos,tipo_aux:Tipos=Tipos.ERROR) -> None:
        self.valor = valor
        self.isTemp = isTemp
        self.tipo = tipo
        if tipo_aux != Tipos.ARREGLO and tipo_aux != Tipos.VECTOR:
            self.tipo_aux = tipo
        else:
            self.tipo_aux = tipo_aux  #para identificar si es un arreglo o no
        self.prof_array=0 #profundidad de un arreglo
        self.env_aux = None #Enviroments resultados de Structs y Modulos
        self.trueLabel = ""
        self.falseLabel = ""

    def getValue(self) -> str:
        return self.valor
