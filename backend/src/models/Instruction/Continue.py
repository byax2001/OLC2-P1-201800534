from models.Abstract.Instruction import Instruccion


class Continue(Instruccion):
    def __init__(self,line:int, column:int):
        self.linea = line
        self.columna = column
    def ejecutar(self, driver, ts):
        pass

    def v_uso_correcto(self,ts):
        if ts.env != "Loop" or ts.env != "While" or ts.env != "ForIn" or ts.env != "If":
            print("Error continue en un ambito que no es loop")