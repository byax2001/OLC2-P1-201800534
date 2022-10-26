from models.Abstract.Instruction import Instruccion
from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Symbol import Symbols,Symbol
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
        ts.generator=self.generator
        symbol:Symbol=ts.buscarC3d(self.id,tmp_aux=tmpaux)
        if symbol!=None:
            if symbol.mut:
                self.exp.generator=self.generator
                exp:ValC3d=self.exp.generarC3d(ts,ptr)

                if symbol.tipo==exp.tipo:
                    ts.generator=self.generator
                    if len(self.cIndex) == 0 and len(self.cIds) ==0:
                        tvalor = self.generator.newTemp()
                        if exp.tipo != Tipos.BOOLEAN or  exp.tipo_aux not in [Tipos.VECTOR,Tipos.ARREGLO]:
                            self.generator.addExpAsign(target=tvalor,right=exp.valor)
                        else:
                            lsalida = self.generator.addLabel()
                            self.generator.addLabel(exp.trueLabel)
                            self.generator.addExpAsign(target=tvalor,right="1")
                            self.generator.addGoto(lsalida)
                            self.generator.addLabel(exp.falseLabel)
                            self.generator.addExpAsign(target=tvalor,right="0")
                            self.generator.addLabel(lsalida)

                        self.generator.addBackStack(index=tmpaux)
                        #ASIGNACION NORMAL: var = val
                        ts.actualizarC3d(id=self.id, value=tvalor)
                        self.generator.addNextStack(index=tmpaux)
                    elif len(self.cIds) ==0: #array[x]==val   len (CIDS) ==0
                        self.generator.addComment("Asignacion al elemento de un arreglo o vector")
                        if symbol.tsimbolo in [Symbols.VECTOR, Symbols.ARREGLO]:
                            if len(self.cIndex) <= symbol.value.profundidad:
                                if len(self.cIndex)<symbol.value.profundidad and exp.tipo_aux not in [Tipos.VECTOR,Tipos.ARREGLO]:
                                    # [[1,2],2,[2,3]]
                                    error = "intento de asignar un elemento no arreglo en una parte no correcta"
                                    print(error)
                                else:
                                    #ASIGNAR
                                    aux_index = self.generator.newTemp()
                                    t_puntero = self.generator.newTemp()
                                    t_tam = self.generator.newTemp()
                                    tvalor = self.generator.newTemp()  # valor del array buscado actualmente
                                    taux = self.generator.newTemp()  # suma del puntero y el index actual
                                    lerror = self.generator.newLabel()
                                    lsalida = self.generator.newLabel()
                                    self.generator.addBackStack(tmpaux)
                                    self.generator.addExpression(target=aux_index, left="P", right=str(symbol.position),
                                                                 operator="+")
                                    self.generator.addNextStack(tmpaux)
                                    self.generator.addGetStack(target=t_puntero, index=aux_index)
                                    if symbol.paso_parametro:  # si fue declarado como paso de parametro en el anterior puntero esta la direccion del verdadero array
                                        # ubicado en el stack
                                        self.generator.addGetStack(target=t_puntero, index=t_puntero)
                                    self.generator.addComment("Tamanio")
                                    self.generator.addGetHeap(target=t_tam, index=t_puntero)
                                    self.generator.incVar(t_puntero)
                                    if symbol.tsimbolo == Symbols.VECTOR:
                                        self.generator.addComment("Saltarse el capacity")
                                        self.generator.incVar(t_puntero)  # saltarse el capacity
                                    x = 0
                                    for index in self.cIndex:
                                        x += 1
                                        index.generator = self.generator
                                        indexR: ValC3d = index.generarC3d(ts, ptr)
                                        self.generator.addIf(left=indexR.valor, rigth=t_tam, operator=">=",
                                                             label=lerror)
                                        self.generator.addIf(left=indexR.valor, rigth="0", operator="<", label=lerror)
                                        #TAUX TIENE EL INDEX PARA ASIGNAR REQUERIDO:  T[AUX] = VAL A ASIGNAR
                                        self.generator.addExpression(target=taux, left=t_puntero, right=indexR.valor,
                                                                     operator="+")  # taux= tpuntero + index

                                        if x != len(self.cIndex):
                                            #SI ACASO EL ARRAY ES DE MAS DIMENSIONES, en la posicion del heap actual
                                            #estara la direccion de otro vector
                                            self.generator.addGetHeap(target=t_puntero, index=taux)  # tpuntero = Heap[taux]
                                            self.generator.addComment("Tamanio")
                                            self.generator.addGetHeap(target=t_tam,
                                                                      index=t_puntero)  # t_tam = Heap[tpuntero]
                                            self.generator.incVar(t_puntero)  # tpuntero = tpuntero +1
                                            if symbol.tsimbolo == Symbols.VECTOR:
                                                self.generator.incVar(t_puntero)
                                    self.generator.addComment("Asignacion al elemento del vector")
                                    self.generator.addSetHeap(index=taux,value=exp.valor)
                                    self.generator.addGoto(lsalida)  # goto Lsalida;
                                    # EN CASO LOS INDEX DEN ERROR:
                                    self.generator.addLabel(lerror)  # Lerror:
                                    self.generator.addError("Bound Error")  # print error
                                    self.generator.addNewLine()
                                    self.generator.addLabel(lsalida)
                            else:
                                self.generator.addError(f"Bounds Error")
                                self.generator.addNewLine()
                                error = "Intento de ingresar a una profundidad mayor a la que posee el array"
                                print(error)
                                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                                  columna=self.columna)
                        else:
                            error = "No se puede asignar de esa forma a una variable no array"
                            print(error)
                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                              columna=self.columna)
                    else:
                        #PARA EL var.dato = val  existe una clase llamada modivarstruct
                        # asi que fijo aca va a ser id[x].val = val
                        if symbol.tsimbolo == [Symbols.VECTOR, Symbols.ARREGLO]:
                            if len(self.cIndex) <= symbol.value.profundidad:
                                #PENDIENTE
                                print()
                            else:
                                self.generator.addError(f"Bounds Error")
                                self.generator.addNewLine()
                                error = "Intento de ingresar a una profundidad mayor a la que posee el array"
                                print(error)
                                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                                  columna=self.columna)
                        else:
                            error = "No se puede asignar de esa forma a una variable no array"
                            print(error)
                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                              columna=self.columna)

                else:
                    error = f"La variable no es del mismo tipo al valor a asignar {self.id}"
                    print(error)
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                      columna=self.columna)

            else:
                error=f"La variable no es muteable {self.id}"
                print(error)
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                  columna=self.columna)
        else:
            error=f"dicha variable no existe {self.id}"
            print(error)
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                              columna=self.columna)
        self.generator.addComment("End Asignacion")

    def tSymtValCorrect(self,symbol:Symbol,exp:ValC3d):
        if exp.tipo_aux in [Tipos.ARREGLO,Tipos.VECTOR]:
            if symbol.tsimbolo in [Tipos.VECTOR]:
                print()

