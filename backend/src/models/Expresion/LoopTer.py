from models.Expresion.Expresion import Expresion
from models.Instruction.Instruction import Instruccion
from models.Instruction.Break import Break
from models.Instruction.Continue import Continue
from models.Instruction.Return import Return
from models.TablaSymbols.Tipos import Tipos

class LoopTer(Expresion):
    def __init__(self,bloque:[Instruccion],line:int,column:int):
        self.bloque=bloque
        self.line=line
        self.column=column
    def getValor(self, driver, ts):
        while True:
            for instruccion in self.bloque:
                if isinstance(instruccion, Break):
                    return instruccion.getValor(driver,ts)
                elif isinstance(instruccion, Continue):
                    break;
                elif isinstance(instruccion, Return):
                    print("Error, existe return afuera de una funcion")
                    return
                rInst = instruccion.ejecutar(driver, ts)
                if isinstance(rInst, Break):
                    return rInst.getValor(driver,ts)
                elif isinstance(rInst, Continue):
                    break;
                elif isinstance(rInst, Return):
                    print("Error, existe return afuera de una funcion")
                    return
    def getTipo(self, driver, ts):
        for instruccion in self.bloque:
            if isinstance(instruccion, Break):
                return instruccion.getTipo(driver, ts)
            elif isinstance(instruccion, Return):
                print("Error, existe return afuera de una funcion")
                return Tipos.ERROR
            rInst = instruccion.ejecutar(driver, ts)
            if isinstance(rInst, Break):
                return rInst.getTipo(driver, ts)
            elif isinstance(rInst, Return):
                print("Error, existe return afuera de una funcion")
                return Tipos.ERROR
        return Tipos.ERROR