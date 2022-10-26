from models.Abstract.Expresion import Expresion
from models.Abstract.Instruction import Instruccion
from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Enviroment import Enviroment
from models.Driver import Driver
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d
from models.TablaSymbols.Symbol import Symbol
class ModiVarStruct(Instruccion):
    def __init__(self,idPrincipal:str,cIds:[str],exp:Expresion,line:int,column:int):
        super().__init__()
        self.idPrincipal=idPrincipal
        self.cId=cIds
        self.exp=exp
        self.line=line
        self.column=column

    def ejecutar(self, driver: Driver, ts: Enviroment):
        varSt = ts.buscar(self.idPrincipal)
        v_exp=self.exp.getValor(driver,ts)
        t_exp=self.exp.getTipo(driver,ts)
        if varSt != None:
            if varSt.tipo == Tipos.STRUCT and varSt.mut==True:
                env_struct = varSt.value  # el valor de cada variable objeto struct es un enviroment el cual se consulta
                symbol=0
                for x in range(len(self.cId)):
                    env = env_struct.buscar(self.cId[x])
                    if env != None:
                        if env.tipo==Tipos.STRUCT:
                            env_struct=env.value
                            if x==len(self.cId)-1:
                                symbol=env
                        else:
                            if x==len(self.cId)-1:
                                symbol=env
                            else:
                                print("Error: La variable no cuenta con el resto de parametros solicitados")
                                error = "Error: La variable no cuenta con el resto de parametros solicitados"
                                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                                  columna=self.column)
                                return
                    else:
                        print(f"Error dicho parametro no existe en el objeto {self.cId[x]}")
                        error = "Error dicho parametro no existe en el objeto"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                          columna=self.column)
                        return
                if symbol.tipo==t_exp:
                    symbol.value=v_exp
                    print("Asignacion realizada")
                else:
                    print("La variable a asignar para el parametro no son del mismo tipo")
                    error = "La variable a asignar para el parametro no son del mismo tipo"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
            else:
                print("Error la variable a usar como objeto struct no lo es o no es muteable")
                error = "Error la variable a usar como objeto struct no lo es o no es muteable"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        else:
            print("Error variable a obtener valor no existe")
            error = "Error variable a obtener valor no existe"
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
    def generarC3d(self,ts:Enviroment,ptr):
        self.generator.addComment("ASIGNACION VAR STRUCT")
        self.exp.generator=self.generator
        ts.generator = self.generator
        tmp_aux = self.generator.newTemp()
        exp:ValC3d = self.exp.generarC3d(ts,ptr)
        varSt:Symbol = ts.buscarC3d(self.idPrincipal,tmp_aux)
        v_exp = exp.valor
        t_exp = exp.tipo
        if varSt != None:
            if varSt.tipo == Tipos.STRUCT and varSt.mut == True:
                if t_exp == Tipos.BOOLEAN:
                    tmp_bool = self.generator.newTemp()
                    lsalida = self.generator.newLabel()
                    self.generator.addLabel(exp.trueLabel)
                    self.generator.addExpAsign(target=tmp_bool,right="1")
                    self.generator.addGoto(lsalida)
                    self.generator.addLabel(exp.falseLabel)
                    self.generator.addExpAsign(target=tmp_bool,right="0")
                    self.generator.addLabel(lsalida)
                    v_exp=tmp_bool

                #PARA CONOCER LA POSICION DEL LA VARIABLE EN EL STRUCT
                env_struct:Enviroment = varSt.env_aux # el valor de cada variable objeto struct es un enviroment el cual se consulta
                symbol = 0
                for x in range(len(self.cId)):
                    env = env_struct.buscar(self.cId[x])
                    if env != None:
                        if env.tipo == Tipos.STRUCT:
                            env_struct = env.env_aux
                            if x == len(self.cId) - 1:
                                symbol = env
                        else:
                            if x == len(self.cId) - 1:
                                symbol = env
                            else:
                                error = "Error: La variable no cuenta con el resto de parametros solicitados"
                                print(error)
                                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                                  columna=self.column)
                                return
                    else:
                        print(f"Error dicho parametro no existe en el objeto {self.cId[x]}")
                        error = "Error dicho parametro no existe en el objeto"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                          columna=self.column)
                        return
                if symbol.tipo == t_exp:
                    aux_index = self.generator.newTemp()
                    self.generator.addComment("Asignacion a la variable en el struct")
                    t_puntero = self.generator.newTemp()
                    self.generator.addBackStack(tmp_aux)
                    # tpuntero index del heap en el stack
                    self.generator.addExpression(target=aux_index,left="P",right=str(varSt.position),operator="+")
                    self.generator.addNextStack(tmp_aux)
                    self.generator.addGetStack(target=t_puntero, index=aux_index)
                    # tpuntero primera posicion del struct
                    self.generator.addExpression(target=t_puntero,left=t_puntero,right=str(symbol.position),operator="+")
                    self.generator.addSetHeap(index=t_puntero,value=v_exp)
                    print("Asignacion realizada")
                else:
                    error = "La variable a asignar para el parametro no son del mismo tipo"
                    print(error)
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
            else:
                error = "Error la variable a usar como objeto struct no lo es o no es muteable"
                print(error)
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        else:
            error = "Error variable a obtener valor no existe"
            print(error)
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)

