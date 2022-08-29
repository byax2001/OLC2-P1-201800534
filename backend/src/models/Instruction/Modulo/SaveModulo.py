from models.Instruction.Instruction import Instruccion
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.Tipos import Tipos
from models.Driver import Driver
from models.TablaSymbols.Symbol import Symbol

class SaveModulo(Instruccion):
    def __init__(self,id:str,cInst:[Instruccion],line:int,column:int):
        self.id=id
        self.cInst=cInst
        self.line=line
        self.column=column
        self.tacceso=0
    def ejecutar(self, driver: Driver, ts: Enviroment):
        existe=ts.buscar(self.id)
        newts=Enviroment(ts,"Modulo")
        if existe==None:
            for ins in self.cInst:
                ins.ejecutar(driver,newts);
            symbol=Symbol(mut=False,id=self.id,value=newts,tipo_simbolo=5,tipo=Tipos.MODULO,line=self.line,
                          column=self.column,tacceso=self.tacceso)
            ts.addVar(self.id,symbol)
        else:
            print("Error id ya ha sido declarado en otra variable")
    def changeAcces(self,acceso:int):
        self.tacceso=acceso