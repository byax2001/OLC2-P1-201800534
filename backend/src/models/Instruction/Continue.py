from models.Instruction.Instruction import Instruccion


class Continue(Instruccion):
    def __init__(self,linea:int, columna:int):
        self.linea = linea
        self.columna = columna
    def ejecutar(self, driver, ts):
        pass