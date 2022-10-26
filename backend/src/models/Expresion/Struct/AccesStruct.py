from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Enviroment import Enviroment
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d
from models.TablaSymbols.Symbol import Symbol,Symbols


class AccesStruct(Expresion):
    def __init__(self,idPrincipal:str,cIds:[str],line:int,column:int):
        super().__init__()
        self.value=None
        self.tipo=None
        self.idPrincipal=idPrincipal
        self.cId=cIds
        self.line=line
        self.column=column
        self.instancia=0

    def getValor(self, driver, ts:Enviroment):
        self.instancia+=1
        if self.value == None and self.tipo == None:
            varSt=ts.buscar(self.idPrincipal)
            if varSt!=None:
                if varSt.tipo==Tipos.STRUCT:
                    env_struct=varSt.value # el valor de cada variable objeto struct es un enviroment el cual se consulta
                    for x in range(len(self.cId)):
                        env = env_struct.buscar(self.cId[x])
                        if env!=None:
                            if env.tipo==Tipos.STRUCT:
                                env_struct=env.value
                                if x == (len(self.cId)-1): #devolvera un enviroment
                                    self.value=env.value
                                    self.tipo=env.tipo
                            else:
                                if x == (len(self.cId)-1): #devolvera un valor primitivo
                                    self.value=env.value
                                    self.tipo=env.tipo
                                else:
                                    self.value==None
                                    error = "La variable no posee dichos componentes"
                                    print(error)
                                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                                      columna=self.column)

                        else:
                            print(f"Error dicho parametro no existe en el objeto {self.cId[x]}")
                            error = "Error dicho parametro no existe en el objeto "
                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                              columna=self.column)
                else:
                    print("Error la variable a usar como objeto struct no lo es")
                    error = "Error la variable a usar como objeto struct no lo es "
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
            else:
                print("Error variable a obtener valor no existe")
                error = "Error variable a obtener valor no existe "
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)

        return self.value

    def getTipo(self, driver, ts):
        self.resetInst()
        if self.value == None and self.tipo == None:
            self.getValor(driver, ts)
            if self.value == None:
                self.tipo = Tipos.ERROR
        else:
            self.instancia+=1
        return self.tipo
    def ejecutar(self,driver,ts):
        pass

    def resetInst(self):
        if self.instancia>1:
            self.instancia=0
            self.value=None
            self.tipo=None

    def generarC3d(self,ts,ptr):
        self.generator.addComment("Acceder a elementos de un var Struct")
        ts.generator = self.generator
        if self.trueLabel=="":
            self.trueLabel= self.generator.newLabel()
        if self.falseLabel=="":
            self.falseLabel= self.generator.newLabel()
        result = ValC3d(valor="0",isTemp=False,tipo=Tipos.INT64)

        tmp_aux = self.generator.newTemp()

        varSt: Symbol = ts.buscarC3d(self.idPrincipal, tmp_aux)
        if varSt != None:
            if varSt.tipo == Tipos.STRUCT:
                tmpR = self.generator.newTemp()
                # PARA CONOCER LA POSICION DEL LA VARIABLE EN EL STRUCT
                env_struct: Enviroment = varSt.env_aux  # el valor de cada variable objeto struct es un enviroment el cual se consulta
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

                    aux_index = self.generator.newTemp()
                    self.generator.addComment("Obtener valor del elemento struct")
                    t_puntero = self.generator.newTemp()
                    self.generator.addBackStack(tmp_aux)
                    # tpuntero index del heap en el stack
                    self.generator.addExpression(target=aux_index, left="P", right=str(varSt.position), operator="+")
                    self.generator.addNextStack(tmp_aux)
                    self.generator.addGetStack(target=t_puntero, index=aux_index)
                    # tpuntero primera posicion del struct
                    self.generator.addExpression(target=t_puntero, left=t_puntero, right=str(symbol.position),
                                                 operator="+")
                    self.generator.addGetHeap(target=tmpR,index=t_puntero)
                    if symbol.tipo == Tipos.BOOLEAN and symbol.tsimbolo not in [Symbols.VECTOR,Symbols.ARREGLO]:
                        self.generator.addIf(left=tmpR,rigth="1",operator=self.trueLabel)
                        self.generator.addGoto(self.falseLabel)
                    result.valor= tmpR
                    result.trueLabel=self.trueLabel
                    result.falseLabel=self.falseLabel
                    result.tipo=symbol.tipo
                    result.tipo_aux=symbol.tipo
                    result.isTemp = True
                    if symbol.tsimbolo ==Symbols.VECTOR:
                        result.prof_array = symbol.value.profundidad
                        result.tipo_aux = Tipos.VECTOR
                    elif symbol.tsimbolo ==Symbols.ARREGLO:
                        result.prof_array = symbol.value.profundidad
                        result.tipo_aux = Tipos.ARREGLO
            else:
                error = "Error la variable a usar como objeto struct no lo es"
                print(error)
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        else:
            error = "Error variable a obtener valor no existe"
            print(error)
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
        return result