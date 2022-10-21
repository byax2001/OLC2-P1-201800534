from models.Abstract.Instruction import Instruccion
from models.Expresion.Vector.vecI import vecI
from models.Abstract.Expresion import Expresion
from models.Expresion.Vector.Vector import Vector
from models.Expresion.Vector.VectorC3d import VectorC3d
from models.TablaSymbols.Symbol import Symbol
from models.TablaSymbols.Tipos import Tipos,getTipo
from models.Driver import Driver
from models.TablaSymbols.Enviroment import Enviroment
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d
#dec vector vacio
class DecVector(Instruccion):
    def __init__(self,mut:bool,id,tipo, vecI:vecI,capacity:Expresion,line:int,column:int):
        super().__init__()
        self.id=id
        self.mut = mut
        self.vecI=vecI
        self.capacity=capacity
        self.tipo =getTipo(tipo) if tipo!=None else None
        self.line=line
        self.column=column
        self.tacceso = 0  #publico por default
        # DECLARACION CON PASO DE PARAMETRO
        self.dec_paso_parametro = False
        # cambio de entorno
        self.puntero_entorno_nuevo = ""
        self.en_funcion = False

    def ejecutar(self, driver: Driver, ts: Enviroment):
        existe=ts.buscarActualTs(self.id)
        if existe==None:
            if self.vecI!=None and self.capacity==None:  #se creo el vector con vec!----------
                tvec = self.vecI.getTipo(driver, ts)
                v_vec=self.vecI.getValor(driver,ts)
                if tvec!=Tipos.ERROR and v_vec!=None:

                    if self.tipo==None:
                        newVec=Vector(vec=v_vec,stateCap=False,capacity=0)
                        symbol=Symbol(mut=self.mut,id=self.id,value=newVec,tipo_simbolo=3,tipo=tvec,line=self.line,
                                      column=self.column,tacceso=self.tacceso)
                        ts.addVar(self.id,symbol)
                        print("Se declaro un vector con \"vec!\"")
                        B_datos().appendVar(id=self.id, t_simbolo=symbol.tsimbolo, t_dato=symbol.tipo, ambito=ts.env,
                                          fila=self.line,
                                          columna=self.column)
                    else:
                        if self.tipo==tvec:
                            newVec = Vector(vec=v_vec, stateCap=False, capacity=0)
                            symbol = Symbol(mut=self.mut, id=self.id, value=newVec, tipo_simbolo=3, tipo=tvec,
                                            line=self.line,
                                            column=self.column, tacceso=self.tacceso)
                            ts.addVar(self.id, symbol)
                            print("Se declaro un vector con \"vec!\"")
                            B_datos().appendVar(id=self.id, t_simbolo=symbol.tsimbolo, t_dato=symbol.tipo, ambito=ts.env,
                                              fila=self.line,
                                              columna=self.column)
                        else:
                            print("el tipo de variable declarado y de vec! no son iguales")
                            error = "el tipo de variable declarado y de vec! no son iguales"
                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                              columna=self.column)
                else:
                    print("declaracion vec! dio error")
                    error = "Error declaracion vec! dio error"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
            elif self.capacity!=None:  #con capacity-------------------------------------------
                tcap = self.capacity.getTipo(driver, ts)
                cap=self.capacity.getValor(driver,ts)
                if tcap==Tipos.INT64 or tcap==Tipos.USIZE:
                    vec=[]
                    newVec=Vector(vec=vec,stateCap=True,capacity=cap)
                    symbol = Symbol(mut=self.mut, id=self.id, value=newVec, tipo_simbolo=3, tipo=self.tipo,
                                    line=self.line,column=self.column,tacceso=self.tacceso)
                    ts.addVar(self.id, symbol)
                    print("Se declaro un vector con \"with_capacity()\"")
                    B_datos().appendVar(id=self.id, t_simbolo=symbol.tsimbolo, t_dato=symbol.tipo, ambito=ts.env,
                                      fila=self.line,
                                      columna=self.column)
                else:
                    print(f"Error la capacidad indicada no es un entero linea: {self.line}")
                    error = "Error la capacidad indicada no es un entero"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
            else:  #con new--------------------------------------------------------------------
                newVec = Vector(vec=[], stateCap=False, capacity=0)
                symbol = Symbol(mut=self.mut, id=self.id, value=newVec, tipo_simbolo=3, tipo=self.tipo,
                                line=self.line,column=self.column,tacceso=self.tacceso)
                ts.addVar(self.id, symbol)
                print("Se declaro un vector con \"new()\"")
                B_datos().appendVar(id=self.id, t_simbolo=symbol.tsimbolo, t_dato=symbol.tipo, ambito=ts.env,
                                  fila=self.line,
                                  columna=self.column)
        else:
            print(f"La id del vector a declarar ya ha sido declarado con anterioridad linea: {self.line}")
            error = "La id del vector a declarar ya ha sido declarado con anterioridad"
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)

    def rVector(self,tipo,nveces):
        vector=[]
        valor=self.valueDefault(tipo)
        for x in range(nveces):
            vector.append({"valor":valor,"tipo":tipo})
        return vector

    def valueDefault(self, tipo:Tipos):
        if(tipo==Tipos.INT64):
            return 0
        elif(tipo==Tipos.FLOAT64):
            return 0.0
        elif (tipo==Tipos.BOOLEAN):
            return False
        elif (tipo==Tipos.STR):
            return ""
        elif (tipo==Tipos.STRING):
            return ""
        elif (tipo==Tipos.CHAR):
            return "\0"
    def changeExp(self,exp:Expresion):
        self.vecI=exp

    def changeAcces(self,acceso:int):
        self.tacceso=acceso

    def generarC3d(self,ts,ptr):
        self.generator.addComment(f"Declaracion de Vector: {self.id}")
        Puntero = "P"
        if self.en_funcion:#EN EL CASO SEA UNA DECLARACION ANTES DE LLAMAR A UNA FUNCION SE CAMBIA EL TIPO DE PUNTERO
                            # DE P   a   tn   (tn=P+ts.size)
            Puntero = self.puntero_entorno_nuevo

        if self.dec_paso_parametro:#SI LA DECLARACION ES UN PASO DE PARAMETRO, SE LE DEBE DE INDICAR A LA
                                   #EXPRESION QUE DEBERA DE RETORNAR LA DIRECCION Y NO EL VALOR
            self.array.paso_parametro = True
        #con vec!--------------------------------------------------------------------
        if self.vecI!=None:
            self.generator.addComment("Vector con vec!")
            self.vecI.generator=self.generator
            vecIr:ValC3d= self.vecI.generarC3d(ts,ptr)
            if self.tipo==None:
                newVec = VectorC3d(vec=vecIr.valor, profundidad=vecIr.prof_array+1)
                symbol = Symbol(mut=self.mut, id=self.id, value=newVec, tipo_simbolo=3, tipo=vecIr.tipo, line=self.line,
                                column=self.column, tacceso=self.tacceso)
                symbol.paso_parametro=self.dec_paso_parametro #por si acaso es una declaracion con paso de parametro

                rDec=ts.addVar(self.id, symbol)
                aux_index=self.generator.newTemp()
                self.generator.addExpression(target=aux_index, left=Puntero, right=str(rDec.position), operator="+")#taux=P+pos
                self.generator.addSetStack(index=aux_index, value=vecIr.valor)  # Stack[(int)pos]= val

                print("Se declaro un vector con \"vec!\"")
                B_datos().appendVar(id=self.id, t_simbolo=symbol.tsimbolo, t_dato=symbol.tipo, ambito=ts.env,
                                    fila=self.line, columna=self.column)
            else:
                if self.tipo==vecIr.tipo:
                    newVec = VectorC3d(vec=vecIr.valor, profundidad=vecIr.prof_array+1)
                    symbol = Symbol(mut=self.mut, id=self.id, value=newVec, tipo_simbolo=3, tipo=vecIr.tipo,
                                    line=self.line,
                                    column=self.column, tacceso=self.tacceso)
                    symbol.paso_parametro = self.dec_paso_parametro  # por si acaso es una declaracion con paso de parametro
                    rDec = ts.addVar(self.id, symbol)
                    aux_index = self.generator.newTemp()
                    self.generator.addExpression(target=aux_index, left=Puntero, right=str(rDec.position), operator="+")#taux=P+pos
                    self.generator.addSetStack(index=aux_index, value=vecIr.valor)  # Stack[(int)pos]= val

                    print("Se declaro un vector con \"vec!\"")
                    B_datos().appendVar(id=self.id, t_simbolo=symbol.tsimbolo, t_dato=symbol.tipo, ambito=ts.env,
                                        fila=self.line, columna=self.column)
                else:
                    error="El tipo de arreglo no es igual al tipo de variable que lo guardara"
                    print(error)
        elif self.capacity!=None:
            self.generator.addComment("Vector con Capacity")
            self.capacity.generator=self.generator
            vecIr: ValC3d = self.capacity.generarC3d(ts, ptr)
            if vecIr in [Tipos.INT64,Tipos.USIZE]:
                tvector=self.generator.newTemp()
                loop=self.generator.newLabel()
                tcont=self.generator.newTemp()
                tvalor=self.generator.newTemp()
                lsalida=self.generator.newLabel()
                self.generator.addExpAsign(target=tvector, right="H")  # tr=H  (inicio del arreglo)
                self.generator.addComment("Tamanio del arreglo")
                self.generator.addSetHeap(index="H",value="0") # Heap[H]=tam arreglo
                self.generator.addNextHeap() #H=H+1
                self.generator.addComment("Capacity")
                self.generator.addSetHeap(index="H", value=vecIr.valor)
                self.generator.addNextHeap()  # H=H+1
                self.generator.addComment("------------------")

                #self.generator.addExpAsign(target=tvalor,right=vecIr.valor)#tvalor=valor
                #self.generator.addExpAsign(target=tcont,right="0")# tcont=0
                #self.generator.addLabel(loop)#Loop:
                #self.generator.addIf(left=tcont,rigth=tvalor,operator=">=",label=lsalida)#if (tcont>=tvalor) goto Lsalida
                #self.generator.addNextHeap()#H=H+1
                #self.generator.addExpression(target=tcont,left=tcont,right=1,operator="+")#tcont=tcont+1
                #self.generator.addGoto(loop)# goto Loop
                #self.generator.addLabel(lsalida) #Lsalida

                newVec = VectorC3d(vec=tvector, stateCap=True, capacity=vecIr.valor,profundidad=1)
                symbol = Symbol(mut=self.mut, id=self.id, value=newVec, tipo_simbolo=3, tipo=self.tipo,
                                line=self.line, column=self.column, tacceso=self.tacceso)
                symbol.paso_parametro = self.dec_paso_parametro  # por si acaso es una declaracion con paso de parametro
                rDec = ts.addVar(self.id, symbol)
                aux_index = self.generator.newTemp()
                self.generator.addExpression(target=aux_index, left=Puntero, right=str(rDec.position), operator="+")
                self.generator.addSetStack(index=aux_index, value=tvector)  # Stack[(int)pos]= punterVector

                print("Se declaro un vector con \"with_capacity()\"")
                B_datos().appendVar(id=self.id, t_simbolo=symbol.tsimbolo, t_dato=symbol.tipo, ambito=ts.env,
                                    fila=self.line,columna=self.column)
            else:
                print(f"Error la capacidad indicada no es un entero linea: {self.line}")
                error = "Error la capacidad indicada no es un entero"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        else:# con new
            self.generator.addComment("Vector con New")
            tvector=self.generator.newTemp()
            self.generator.addExpAsign(target=tvector, right="H")  # tr=H  (inicio del arreglo)
            self.generator.addComment("tamanio Vector")
            self.generator.addSetHeap(index="H", value="0")  # Heap[H]=tam arreglo
            self.generator.addNextHeap()  # H=H+1
            self.generator.addComment("Capacity Vector")
            self.generator.addSetHeap(index="H", value="0")  # Heap[H]=tam arreglo
            self.generator.addNextHeap()  # H=H+1
            self.generator.addComment("--------------")


            newVec = VectorC3d(vec=tvector, stateCap=False, capacity="0", profundidad=1)
            symbol = Symbol(mut=self.mut, id=self.id, value=newVec, tipo_simbolo=3, tipo=self.tipo,
                            line=self.line, column=self.column, tacceso=self.tacceso)
            symbol.paso_parametro = self.dec_paso_parametro  # por si acaso es una declaracion con paso de parametro
            rDec = ts.addVar(self.id, symbol)
            aux_index = self.generator.newTemp()
            self.generator.addExpression(target=aux_index, left=Puntero, right=str(rDec.position), operator="+")
            self.generator.addSetStack(index=aux_index, value=tvector)  # Stack[(int)pos]= punterVector


            print("Se declaro un vector con \"new()\"")
            B_datos().appendVar(id=self.id, t_simbolo=symbol.tsimbolo, t_dato=symbol.tipo, ambito=ts.env,
                                fila=self.line, columna=self.column)