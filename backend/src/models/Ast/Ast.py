from models.Instruction.Return import Return
from models.Instruction.Break import Break
from models.Instruction.Continue import Continue
from Generator3D.Generator3D import Generator
class Ast:

    def __init__(self, instrucciones=None):
        if instrucciones is None:
            instrucciones = []
        self.instrucciones = instrucciones

    def ejecutar(self, driver, ts, generator):

        for instruccion in self.instrucciones:
            try:
                if isinstance(instruccion,Break) or isinstance(instruccion,Continue) or isinstance(instruccion,Return):
                    print("Error existen breaks, continues y returns en el entorno global")
                instruccion.generator=generator
                rInst=instruccion.ejecutar(driver, ts)
                if isinstance(rInst,Break) or isinstance(rInst,Continue) or isinstance(rInst,Return):
                    print("Error existen Instrucciones que retornan breaks, continues y returns en el entorno global")
            except Exception as e:
                print(f"hubo un error {e}")
        return generator.getCode()
