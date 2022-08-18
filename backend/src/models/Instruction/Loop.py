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
            new_ts= Enviroment(ts,"Loop");
            for instruccion in self.bloque:
                if isinstance(instruccion, Break):
                    return
                elif isinstance(instruccion, Continue):
                    break;
                elif isinstance(instruccion, Return):
                    print("Error, existe return afuera de una funcion")
                    return
                rInst = instruccion.ejecutar(driver,new_ts)
                if isinstance(rInst, Break):
                    return
                elif isinstance(rInst, Continue):
                    break;
                elif isinstance(rInst, Return):
                    print("Error, existe return afuera de una funcion")
                    return
    #esto solo se usara cuando se use como expresion
    def getValor(self, driver, ts):
        if self.value==None:
            while True:
                for instruccion in self.bloque:
                    if isinstance(instruccion, Break):
                        self.value=instruccion.getValor(driver,ts)
                        self.tipo=instruccion.getTipo(driver,ts)
                        return self.value
                    elif isinstance(instruccion, Continue):
                        break
                    elif isinstance(instruccion, Return):
                        print("Error, existe return afuera de una funcion")
                        return
                    rInst = instruccion.ejecutar(driver, ts)
                    if isinstance(rInst, Break):
                        self.value = rInst.getValor(driver, ts)
                        self.tipo = rInst.getTipo(driver, ts)
                        return self.value
                    elif isinstance(rInst, Continue):
                        break
                    elif isinstance(rInst, Return):
                        print("Error, existe return afuera de una funcion")
                        return
        else:
            return self.value
    def getTipo(self, driver, ts):
        if self.tipo== None:
            self.getValor(driver,ts)
            if self.tipo==None: #si despues de eso sigue siendo None, significa que ocurrio un error
                self.tipo=Tipos.ERROR
            return self.tipo
        else:
            return self.tipo