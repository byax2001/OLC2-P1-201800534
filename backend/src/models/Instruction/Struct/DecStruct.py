from models.Instruction.Instruction import Instruccion
from models.Driver import Driver
from models.TablaSymbols.Enviroment import Enviroment
from models.Expresion.Struct.ExpStruct import ExpStruct
from models.TablaSymbols.Symbol import Symbol,Symbols
from models.TablaSymbols.Tipos import Tipos
from models.Expresion.Expresion import Expresion

class DecStruct(Instruccion):
    def __init__(self,mut, id, exp:ExpStruct, line: int, column: int):
        self.mut=mut
        self.id = id
        self.exp=exp
        self.line=line
        self.column=column
        self.tacceso = 0 #publico por default
    #  let id =     id       { var : valor , var2: valor }
    #      id      idStruct
    #  let id : tipostruct (id) =     id       { var : valor , var2: valor }
    #      id      idStruct             expsStruct

    def ejecutar(self, driver: Driver, ts: Enviroment):
        existe=ts.buscarActualTs(self.id)
        if existe==None:

            t_exp = self.exp.getTipo(driver, ts)
            v_exp=self.exp.getValor(driver,ts)
            if t_exp==Tipos.STRUCT:
                    # lo que guardaran los structs son enviroments nuevos donde se podra consultar las variables en posteriores ocasiones
                    symbol = Symbol(mut=self.mut, id=self.mut, value=v_exp, tipo_simbolo=4, tipo=Tipos.STRUCT,
                                    line=self.line, column=self.column,tacceso=self.tacceso)
                    ts.addVar(self.id, symbol)
                    print("Variable struct declarada")
            else:
                print("Error el struct a declarar da error")
        else:
            print("Error la variable ya ha sido declarada")
    def changeExp(self,exp:Expresion):
        self.exp=exp
    def changeAcces(self,acceso:int):
        self.tacceso=acceso