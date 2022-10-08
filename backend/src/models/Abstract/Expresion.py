from Generator3D.Generator3D import Generator
class Expresion:
    def __init__(self)->None:
        super().__init__()
        self.generator=Generator()
        self.trueLabel = ""
        self.falseLabel = ""

    def getTipo(self, driver, ts):
        """
        Returna el tipo de la expresión
        """
        pass

    def getValor(self, driver, ts):
        """
        Returna el valor de la expresión
        """
        pass
    def ejecutar(self,driver,ts):
        """por si fuera necesario ejecutar algo"""
        pass
    def generarC3d(self,ts,ptr):
        pass