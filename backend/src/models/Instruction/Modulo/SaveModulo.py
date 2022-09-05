from models.Instruction.Instruction import Instruccion
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.Tipos import Tipos
from models.Driver import Driver
from models.TablaSymbols.Symbol import Symbol
from BaseDatos.B_datos import B_datos
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
            print(f"Modulo declarado {self.id}")
            B_datos().appendVar(id=self.id, t_simbolo=symbol.tsimbolo, t_dato=symbol.tipo, ambito=ts.env, fila=self.line,
                              columna=self.column)
        else:
            print("Error id ya ha sido declarado en otra variable")
            error = "Error id ya ha sido declarado en otra variable"
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
    def changeAcces(self,acceso:int):
        self.tacceso=acceso