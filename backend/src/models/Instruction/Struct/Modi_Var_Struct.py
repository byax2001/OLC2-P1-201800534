from models.Expresion.Expresion import Expresion
from models.Instruction.Instruction import Instruccion
from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Enviroment import Enviroment
from models.Driver import Driver
from BaseDatos.B_datos import B_datos
class ModiVarStruct(Instruccion):
    def __init__(self,idPrincipal:str,cIds:[str],exp:Expresion,line:int,column:int):
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
