from models.Instruction.Declaracion import Declaracion
from Generator3D.Generator3D import Generator
class Struct:
    def __init__(self,cDec:[Declaracion]):
        self.nDec:[Declaracion]=cDec
        self.size=len(cDec)
    def clearDecs(self):
        for dec in self.nDec:
            dec.changeExp(None)
    def changeExp(self,id,exp):
        for dec in self.nDec:
            if dec.getId()==id and dec.getExp()==None:
                dec.changeExp(exp)
                return True
        return False
    def ejecutarDecs(self,driver,ts):
        for dec in self.nDec:
            stateDec=dec.ejecutar(driver,ts) #en el metodo ejecutar de declaracion si ocurre un error devuelve False, si todo
                                             #ocurrio con normalidad entonces devuelve None
            if stateDec!=None:  #si devuelve Falso y no None es que ocurrio un error al declarar
                return False

    def getSize(self):
        return self.size

    def ejecutarDecsC3d(self,ts,ptr,generator:Generator):
        for dec in self.nDec:
            dec.generator=generator
            dec.decStructsC3d(ts,ptr=ptr) #en el metodo ejecutar de declaracion si ocurre un error devuelve False, si todo
                                           #ocurrio con normalidad entonces devuelve None


