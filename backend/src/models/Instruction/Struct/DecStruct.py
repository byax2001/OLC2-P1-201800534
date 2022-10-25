from models.Abstract.Instruction import Instruccion
from models.Driver import Driver
from models.TablaSymbols.Enviroment import Enviroment
from models.Expresion.Struct.ExpStruct import ExpStruct
from models.TablaSymbols.Symbol import Symbol
from models.TablaSymbols.Tipos import Tipos
from models.Abstract.Expresion import Expresion
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d
from models.TablaSymbols.SymC3d import SymC3d

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
                    B_datos().appendVar(id=self.id, t_simbolo=symbol.tsimbolo, t_dato=symbol.tipo, ambito=ts.env,
                                      fila=self.line,
                                      columna=self.column)
            else:
                print("Error el struct a declarar da error")
                error = "Error el struct a declarar da error"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        else:
            print("Error la variable ya ha sido declarada")
            error = "Error la variable ya ha sido declarada"
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
    def changeExp(self,exp:Expresion):
        self.exp=exp
    def changeAcces(self,acceso:int):
        self.tacceso=acceso
    def generarC3d(self,ts,ptr):
        existe = ts.buscarActualTs(self.id)
        if existe == None:
            self.exp.generator=self.generator
            exp:ValC3d=self.exp.generarC3d(ts,ptr)
            t_exp = exp.tipo
            v_exp = exp.valor
            if t_exp == Tipos.STRUCT:
                # lo que guardaran los structs son enviroments nuevos donde se podra consultar las variables en posteriores ocasiones
                symbol = Symbol(mut=self.mut, id=self.mut, value=v_exp, tipo_simbolo=4, tipo=Tipos.STRUCT,
                                line=self.line, column=self.column, tacceso=self.tacceso)
                symbol.env_aux = exp.env_aux
                temp_var: SymC3d=ts.addVar(self.id, symbol)
                aux_index = self.generator.newTemp()
                Puntero = "P"
                self.generator.addExpression(target=aux_index, left=Puntero, right=str(temp_var.position), operator="+")
                self.generator.addSetStack(index=aux_index, value=str(temp_var.valor))  # Stack[(int)pos]= val
                print("Variable struct declarada")
                B_datos().appendVar(id=self.id, t_simbolo=symbol.tsimbolo, t_dato=symbol.tipo, ambito=ts.env,
                                    fila=self.line,columna=self.column)
            else:
                error = "Error el struct a declarar da error o no es struct"
                print(error)
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        else:
            error = "Error la variable ya ha sido declarada"
            print(error)
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)