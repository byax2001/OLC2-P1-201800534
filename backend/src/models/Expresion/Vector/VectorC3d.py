from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Enviroment import Enviroment
from Generator3D.Generator3D import Generator
class VectorC3d:
    def __init__(self,vec,profundidad=0):
        self.generator=Generator()
        self.vector=vec
        self.ocupado=0
        self.profundidad=profundidad
