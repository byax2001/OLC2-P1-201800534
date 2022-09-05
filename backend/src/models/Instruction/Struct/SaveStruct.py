from models.Instruction.Instruction import Instruccion
from models.Driver import Driver
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Symbol import Symbol
from models.Expresion.Struct.Struct import Struct
from BaseDatos.B_datos import B_datos
class SaveStruct(Instruccion):
    def __init__(self,id:str,cInst:[Instruccion],line:int,column:int):
        self.id=id
        self.cInst=cInst
        self.line=line
        self.column=column
        self.tacceso=0 #publico por default
    def ejecutar(self, driver: Driver, ts: Enviroment):
        symbol=ts.buscarActualTs(self.id)
        if symbol==None:

            #aqui se podria agregar un metodo donde si una declaracion tiene el mismo id que alguna de las anteriores dar error y no declarar el struct

            struct=Struct(self.cInst);
            symbol=Symbol(mut=False,id=self.id,value=struct,tipo_simbolo=4,tipo=Tipos.STRUCT,line=self.line,
                          column=self.column,tacceso=self.tacceso)
            ts.addVar(self.id,symbol)
            print(f"Struct declarado {self.id}")
        else:
            print(f"Error: se intenta declarar un struct con una id ya declarada {self.line}")
            error = "Error: se intenta declarar un struct con una id ya declarada "
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
    def changeAcces(self,acceso:int):
        self.tacceso=acceso