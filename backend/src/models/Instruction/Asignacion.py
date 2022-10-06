from models.Abstract.Instruction import Instruccion
from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Symbol import Symbols
from models.Expresion.Vector.Vector import Vector
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d
from models.TablaSymbols.Enviroment import Enviroment

class Asignacion(Instruccion):
    def __init__(self,id:str,cIndex:[Expresion],cIds:[str],exp: Expresion, linea:int, columna:int):
        super().__init__()
        self.id=id
        self.cIndex=cIndex
        self.cIds=cIds
        self.exp = exp
        self.linea = linea
        self.columna = columna

    def ejecutar(self, driver, ts):
        Symbol=ts.buscar(self.id);
        if Symbol !=None:
            if(Symbol.mut==True):
                if type(self.exp)!=list:
                    t_exp = self.exp.getTipo(driver, ts)
                    v_exp=self.exp.getValor(driver,ts)
                    if v_exp!=None:
                        t_exp=self.auxTipos(Symbol.tipo,v_exp,t_exp)  #para poder poder asignar aun si los tipos no son los mismos
                                                                      #pero son los correctos, como un usize en un entero o viceversa y que el valor sea mayor o igual a 0
                                                                      #si es usize y el tipo simbolo es entero se manipula
                                                                      #el tipo de expresion a como el simbolo requiere por ejemplo

                        if Symbol.tipo == t_exp or Symbol.tipo==Tipos.STRUCT:
                            if len(self.cIndex)==0 and type(v_exp)!=list: #si es una asignacion normal
                                ts.actualizar(self.id,v_exp)
                            else: # si es la asignacion de un vector
                                if Symbol.tsimbolo==Symbols.ARREGLO or Symbol.tsimbolo==Symbols.VECTOR:
                                    vecIndex=[]
                                    for index in self.cIndex:
                                        tipo_index = index.getTipo(driver, ts)
                                        valor_index = index.getValor(driver, ts)
                                        if tipo_index == Tipos.INT64 or tipo_index == Tipos.USIZE:  # cIndex= [expresion,expresion,expresion]
                                            vecIndex.append(valor_index)
                                        else:
                                            print(f"Error: uno de los index no es un entero {self.linea}")
                                            error = "Error: uno de los index no es un entero"
                                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                                              columna=self.columna)
                                            return
                                    if len(self.cIds)==0:    # arreglo[0]= "hola"
                                        l=Symbol.value.updateVector(cIndex=vecIndex,valor=v_exp)
                                        print(l)
                                    else: #arreglo[0].palabra= "hola"
                                        Symbol.value.updateVectorStruct(cIndex=vecIndex,cIds=self.cIds,valor=v_exp,tipo_val=t_exp)
                                else:
                                    print("intento de hacer asignacion de vector a una variable que no lo es")
                                    error = "intento de hacer asignacion de vector a una variable que no lo es"
                                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                                      columna=self.columna)

                        else:
                            print("El valor a asignar es de distinto tipo al de la variable")
                            error = "El valor a asignar es de distinto tipo al de la variable"
                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                              columna=self.columna)

                    else:
                        print("El valor que se intenta asignar a la variable es None o da error")
                        error = "El valor que se intenta asignar a la variable es None o da error"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                          columna=self.columna)
                else:
                    if Symbol.tsimbolo==Symbols.VECTOR or Symbol.tsimbolo==Symbols.ARREGLO:
                        if len(self.exp)==0:
                            newVector=Vector(vec=[],stateCap=True,capacity=0)
                            Symbol.value=newVector
                        else:
                            t_cap=self.exp[0].getTipo(driver,ts)
                            valor=self.exp[0].getValor(driver,ts)
                            newVector = Vector(vec=[], stateCap=True, capacity=valor)
                            Symbol.value=newVector
                    else:
                        print("Esta variable no es un array o vector para poder asignarle dicho valor")
                        error = "Esta variable no es un array o vector para poder asignarle dicho valor"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                          columna=self.columna)
            else:
                print("La variable que intenta cambiar no es muteable")
                error = "La variable que intenta cambiar no es muteable"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                  columna=self.columna)
        else:
            print("No ha sido declarada dicha variable")
            error = "No ha sido declarada dicha variable"
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                              columna=self.columna)
    def auxTipos(self,tipo_sim,valor,t_exp):
        if tipo_sim==Tipos.INT64:
            if t_exp==Tipos.USIZE:
                return Tipos.INT64
        elif tipo_sim==Tipos.USIZE:
            if valor>=0 and t_exp==Tipos.INT64:
                return Tipos.USIZE
        return t_exp

    def generarC3d(self,ts:Enviroment,ptr:int):
        self.generator.addComment("Asignacion")
        tmpaux=self.generator.newTemp()
        symbol=ts.buscarC3d(self.id,tmp_aux=tmpaux)
        if symbol!=None:
            self.exp.generator=self.generator
            exp:ValC3d=self.exp.generarC3d(ts,ptr)
            if symbol.tipo==exp.tipo:
                self.generator.addBackStack(index=tmpaux)
                ts.generator=self.generator
                ts.actualizarC3d(id=self.id,value=exp.valor)
                self.generator.addNextStack(index=tmpaux)
        else:
            error="dicha variable no existe"
            print(error)
        self.generator.addComment("End Asignacion")

