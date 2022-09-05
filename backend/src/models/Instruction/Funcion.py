from models.Instruction.Instruction import Instruccion
from models.Instruction.Declaracion import Declaracion
from models.TablaSymbols.Symbol import Symbol
from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos,getTipo
from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.Tipos import Tipos
from models import Driver
from BaseDatos.B_datos import B_datos


class Funcion(Instruccion):
    def __init__(self,id:str,lparametros:[Declaracion],tipo:str,bloque:[Instruccion], line:int,column:int):
        self.id=id
        self.params=lparametros
        self.tipoFun= getTipo(tipo) if tipo!="" else Tipos.VOID
        self.bloque=bloque
        self.line=line
        self.column=column
        self.tacceso = 0 #publico por default
    def ejecutar(self, driver: Driver, ts: Enviroment):
        existe=ts.buscarActualTs(self.id)
        if existe==None:
            print("Se guardo una funcion")
            newSymbol=Symbol(mut=False,id=self.id,value=[self.params,self.bloque],tipo_simbolo=2,
                             tipo=self.tipoFun,line=self.line,column=self.column,tacceso=self.tacceso)
            ts.addVar(self.id,newSymbol)
        else:
            print("Id ya declarado")
            error = "Id ya declarado"
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
    def changeAcces(self,acceso:int):
        self.tacceso=acceso