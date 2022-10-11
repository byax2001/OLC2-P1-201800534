from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Enviroment import Enviroment
from Generator3D.Generator3D import Generator
class VectorC3d:
    def __init__(self,vec,stateCap,capacity,profundidad=0):
        self.generator=Generator()
        self.vector=vec
        self.stateCap=stateCap #si es false no es necesario verificar si el vector esta lleno o no
        self.capacity=capacity
        self.ocupado=0
        self.profundidad=profundidad

    def len(self):
        t_tam=self.generator.newTemp()
        self.generator.addGetHeap(target=t_tam,index=self.vector) #self.vector sera el puntero