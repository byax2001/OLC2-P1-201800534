from models.Instruction import Instruction


class Ast:

    def __init__(self, instrucciones=None):
        if instrucciones is None:
            instrucciones = []
        self.instrucciones = instrucciones

    def ejecutar(self, driver, ts):
        for instruccion in self.instrucciones:
            try:
                instruccion.ejecutar(driver, ts)
            except:
                print("ocurrio un error")