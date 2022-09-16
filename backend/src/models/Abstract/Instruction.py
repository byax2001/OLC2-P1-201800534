from models.TablaSymbols.Enviroment import Enviroment
from Generator3D.Generator3D import Generator
from models.Driver import Driver


class Instruccion:
    def __init__(self) -> None:
        super().__init__()
        self.generator = Generator()
    def ejecutar(self, driver: Driver, ts: Enviroment):
        pass
    def generarC3d(self,ts,ptr:int):
        pass