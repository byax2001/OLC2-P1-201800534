from models.Abstract.Expresion import Expresion
from models.Driver import Driver
from models.TablaSymbols.Enviroment import Enviroment
from models.Expresion.Struct.ExpStruct import ExpStruct
from models.Expresion.Struct.Struct import Struct
from models.TablaSymbols.Tipos import Tipos
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d

class DecStructExp(Expresion):
    def __init__(self, idStruct: str, expStruct:[ExpStruct], line: int, column: int):
        self.value=None
        self.tipo=None
        self.idSt=idStruct
        self.cExp=expStruct
        self.line=line
        self.column=column
        self.instancia=0

    #  let id =     id       { var : valor , var2: valor }
    #      id      idStruct             expsStruct
    def getValor(self, driver, ts):  #lo que va a retornar va a ser un Enviromet o tabla ts a guardar
        self.instancia+=1
        if self.value==None and self.tipo==None:
            newts = Enviroment(ts, "Struct")
            struct = ts.buscar(self.idSt)
            if struct != None:
                if struct.tipo == Tipos.STRUCT:
                    st: Struct = struct.value
                    st.clearDecs()
                    if len(self.cExp) == st.getSize():
                        for exp in self.cExp:
                            changeExp = st.changeExp(exp.id, exp.exp)
                            if changeExp == False:
                                print("Error al asignar: la variable no existe en el struct solicitado o el tipo de valor no es igual al tipo  de la variable")
                                error = "Error al asignar: la variable no existe en el struct solicitado o el tipo de valor no es igual al tipo  de la variable"
                                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                                  columna=self.column)
                                return
                        # mando a ejecutar el metodo en la clase Struct que ejecuta todas sus declaraciones
                        stateDecs = st.ejecutarDecs(driver, newts)
                        if stateDecs != None:  # si devuelve Falso y no None es que ocurrio un error al declarar
                            print("Ocurrio un error al intentar declarar una variable tipo struct")
                            error = "Ocurrio un error al intentar declarar una variable tipo struct"
                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                              columna=self.column)
                            self.value=None
                        # lo que guardara en las variables struct son enviroments nuevos donde se podra consultar las variables declaradas aqui para manipularlas en posteriores ocasiones
                        self.value=newts
                        self.tipo = Tipos.STRUCT
                    else:
                        print("No tiene la cantidad suficiente de variables declaradas para el struct")
                        error = "No tiene la cantidad suficiente de variables declaradas para el struct"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                          columna=self.column)
                        self.value = None
                else:
                    print("Error el id del struct a declarar en una variable pertenece al id de una variable no struct")
                    error = "Error el id del struct a declarar en una variable pertenece al id de una variable no struct"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
                    self.value = None
            else:
                print("Intento de asignacion de un struct inexistente")
                error = "Intento de asignacion de un struct inexistente"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
                self.value=None
        return self.value

    def getTipo(self, driver, ts):
        self.resetInst()
        if self.value==None and self.tipo==None:
            self.getValor(driver,ts)
            if self.value==None:
                self.tipo=Tipos.ERROR
        else:
            self.instancia+=1
        return self.tipo

    def resetInst(self):
        if self.instancia>1:
            self.instancia=0
            self.value=None
            self.tipo=None

    def ejecutar(self, driver: Driver, ts: Enviroment):
        pass

    def generarC3d(self,ts,ptr):
        self.generator.addComment("Expresion Dec Struct  {id:expresion,id:expresion}")
        ts.generator = self.generator
        tmpR = self.generator.newTemp()
        result = ValC3d(valor=tmpR,isTemp=True,tipo=Tipos.ERROR)
        newts = Enviroment(ts, "Struct")
        struct = ts.buscar(self.idSt)
        if struct != None:
            if struct.tipo == Tipos.STRUCT:
                st: Struct = struct.value
                st.clearDecs()
                if len(self.cExp) == st.getSize():
                    for exp in self.cExp:
                        changeExp = st.changeExp(exp.id, exp.exp)
                        if changeExp == False:
                            error = "Error al asignar: la variable no existe en el struct solicitado o el tipo de valor no es igual al tipo  de la variable"
                            print(error)
                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                              columna=self.column)
                            return result
                    result.tipo=Tipos.STRUCT
                    result.tipo_aux=Tipos.STRUCT
                    result.env_aux = newts
                    self.generator.addExpAsign(target=tmpR,right="H")
                    self.generator.addExpression(target="H",left="H",right=str(len(self.cExp)),operator="+")
                    st.ejecutarDecsC3d(ts=newts,ptr=tmpR,generator=self.generator)
                else:
                    error = "No tiene la cantidad suficiente de variables declaradas para el struct"
                    print(error)
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
            else:
                error = "Error el id del struct a declarar en una variable pertenece al id de una variable no struct"
                print(error)
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
        else:
            error = "Intento de asignacion de un struct inexistente"
            print(error)
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        return result