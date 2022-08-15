from models.Instruction.Instruction import Instruccion
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.Tipos import Tipos
from models.Instruction.Break import Break
from models.Instruction.Continue import Continue
from models.Instruction.Return import Return

class Loop(Instruccion):
    def __init__(self,bloque:[Instruccion],line:int,column:int):
        self.tipo=None
        self.value=None
        self.bloque=bloque
        self.line=line
        self.column=column
    def ejecutar(self, driver, ts: Enviroment):
        while True:
            for instruccion in self.bloque:
                if isinstance(instruccion, Break):
                    return
                elif isinstance(instruccion, Continue):
                    continue
                elif isinstance(instruccion, Return):
                    print("Error, existe return afuera de una funcion")
                    return
                rInst = instruccion.ejecutar(driver, ts)
                if isinstance(rInst, Break):
                    return rInst
                elif isinstance(rInst, Continue):
                    continue
                elif isinstance(rInst, Return):
                    print("Error, existe return afuera de una funcion")
                    return
    #esto solo se usara cuando se use como expresion
    def getValor(self, driver, ts):
        if self.value==None and self.tipo==None:
            while True:
                for instruccion in self.bloque:
                    if isinstance(instruccion, Break):
                        self.value=instruccion.getValor(driver,ts)
                        self.tipo=instruccion.getTipo(driver,ts)
                        return self.value
                    elif isinstance(instruccion, Continue):
                        continue
                    elif isinstance(instruccion, Return):
                        print("Error, existe return afuera de una funcion")
                        return
                    rInst = instruccion.ejecutar(driver, ts)
                    if isinstance(rInst, Break):
                        self.value = rInst.getValor(driver, ts)
                        self.tipo = rInst.getTipo(driver, ts)
                        return self.value
                    elif isinstance(rInst, Continue):
                        continue
                    elif isinstance(rInst, Return):
                        print("Error, existe return afuera de una funcion")
                        return
        else:
            return self.value
    def getTipo(self, driver, ts):
        if self.tipo!= None:
            for instruccion in self.bloque:
                if isinstance(instruccion, Break):
                    self.value = instruccion.getValor(driver, ts)
                    self.tipo = instruccion.getTipo(driver, ts)
                    return self.tipo
                elif isinstance(instruccion, Return):
                    print("Error, existe return afuera de una funcion")
                    return Tipos.ERROR
                rInst = instruccion.ejecutar(driver, ts)
                if isinstance(rInst, Break):
                    self.value = rInst.getValor(driver, ts)
                    self.tipo = rInst.getTipo(driver, ts)
                    return self.tipo
                    return rInst.getTipo(driver, ts)
                elif isinstance(rInst, Return):
                    print("Error, existe return afuera de una funcion")
                    return Tipos.ERROR
            return Tipos.ERROR
        else:
            return self.tipo