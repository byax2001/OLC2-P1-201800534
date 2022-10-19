from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.Symbol import Symbols,Symbol
from models.TablaSymbols.Tipos import Tipos
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d

class AccesVec(Expresion):
    def __init__(self, id: str,cIndex:[Expresion],cIds:[str], line: int, column: int):
        super().__init__()
        self.value=None
        self.tipo=None
        self.id = id
        self.cIndex=cIndex
        self.cIds=cIds
        self.line = line
        self.column = column
        self.instancia=0
    def ejecutar(self,driver,ts):
        pass
    def getValor(self, driver, ts):
        self.instancia += 1
        if self.tipo==None and self.value==None:
            symbol = ts.buscar(self.id)
            vecIndex=[]
            for index in self.cIndex:
                tipo_index=index.getTipo(driver,ts)
                if tipo_index==Tipos.INT64 or tipo_index==Tipos.USIZE:  #cIndex= [expresion,expresion,expresion]
                    vecIndex.append(index.getValor(driver,ts))
                else:
                    print(f"Error: uno de los index no es un entero {self.line}")
                    error = "Error: uno de los index no es un entero "
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
                    return

            if symbol != None:  # si existe el vector, si ya fue declarado
                if symbol.tsimbolo == Symbols.VECTOR or symbol.tsimbolo==Symbols.ARREGLO:  # si lo que se llamo fue un vector o arreglo
                    vector = symbol.value
                    self.value = vector.acces(vecIndex) #Se llama al metodo declarado en la clase Vector para obtener el valor del elemento deseado
                                                            #con los indices especificados.
                    if self.value != None:
                            self.tipo = symbol.tipo
                    else:
                        #mensaje de error en el metoo del vector
                        self.tipo = Tipos.ERROR
                        #HASTA ACA TERMINARIA SI FUERA SOLO arreglo[0]
                        #pero si es arreglo[0].variable entonces hacer lo de abajo
                    if len(self.cIds)>0 and self.tipo==Tipos.STRUCT:
                        objeto:Enviroment=self.value
                        x = 0
                        for id in self.cIds:
                            objeto=objeto.buscar(id)
                            x += 1
                            if objeto.tipo != Tipos.STRUCT and x != len(self.cIds):
                                print("Error la variable no cuenta con tantos parametros anidados")
                                error = "Error la variable no cuenta con tantos parametros anidados"
                                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                                  columna=self.column)
                                return
                        self.value=objeto.value
                        self.tipo=objeto.tipo

                else:
                    print(f"Error Intento de obtener valor en una variable no vectorial  linea:{self.line} ")
                    error = "Error Intento de obtener valor en una variable no vectorial"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
            else:
                print(f"Error Intento de Insert en vector no declarado linea:{self.line} ")
                error = "Error Intento de Insert en vector no declarado linea"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        return self.value
    def getTipo(self, driver, ts):
        self.resetInst()
        if self.value==None and self.tipo==None:
            self.getValor(driver,ts)
            if self.value==None: #si despues de eso aun es None entonces da error al intentar obtener un valor
                self.tipo==Tipos.ERROR
        else:
            self.instancia+=1
        return self.tipo

    def resetInst(self):
        if self.instancia>1:
            self.instancia=0
            self.value=None
            self.tipo=None


    def generarC3d(self,ts:Enviroment,ptr):
        self.generator.addComment("Acceso al elemento de un vector")
        result = ValC3d(valor="0",isTemp=False,tipo=Tipos.INT64)
        tmp_aux=self.generator.newTemp()
        symbol:Symbol = ts.buscarC3d(self.id,tmp_aux)
        if symbol !=None:
            if len(self.cIndex) > symbol.value.profundidad:
                self.generator.addError(f"Bounds Error")
            else:
                result.tipo=symbol.tipo
                aux_index = self.generator.newTemp()
                t_puntero = self.generator.newTemp()
                t_tam = self.generator.newTemp()
                tvalor = self.generator.newTemp() #valor del array buscado actualmente
                taux = self.generator.newTemp() #suma del puntero y el index actual
                lerror = self.generator.newLabel()
                lsalida = self.generator.newLabel()
                self.generator.addBackStack(tmp_aux)
                self.generator.addExpression(target=aux_index,left="P",right=str(symbol.position),operator="+")
                self.generator.addNextStack(tmp_aux)
                self.generator.addGetStack(target=t_puntero,index=aux_index)
                self.generator.addComment("Tamanio")
                self.generator.addGetHeap(target=t_tam,index=t_puntero)
                self.generator.incVar(t_puntero)
                if symbol.tsimbolo == Symbols.VECTOR:
                    self.generator.addComment("Saltarse el capacity")
                    self.generator.incVar(t_puntero) #saltarse el capacity
                x = 0
                for index in self.cIndex:
                    x+=1
                    index.generator=self.generator
                    indexR : ValC3d = index.generarC3d(ts,ptr)
                    self.generator.addIf(left=indexR.valor,rigth=t_tam,operator=">=",label=lerror)
                    self.generator.addIf(left=indexR.valor, rigth="0", operator="<", label=lerror)
                    self.generator.addExpression(target=taux,left=t_puntero,right=indexR.valor,operator="+")#taux= tpuntero + index
                    self.generator.addGetHeap(target=tvalor,index=taux) #tvalor = Heap[taux]
                    if x!=len(self.cIndex):
                        self.generator.addExpAsign(target=t_puntero,right=tvalor) #tpuntero = tvalor
                        self.generator.addComment("Tamanio")
                        self.generator.addGetHeap(target=t_tam,index=t_puntero) # t_tam = Heap[tpuntero]
                        self.generator.incVar(t_puntero) # tpuntero = tpuntero +1
                        if symbol.tsimbolo == Symbols.VECTOR:
                            self.generator.incVar(t_puntero)
                result.valor=tvalor
                result.isTemp=True
                self.generator.addGoto(lsalida)# goto Lsalida;
                #EN CASO LOS INDEX DEN ERROR:
                self.generator.addLabel(lerror) #Lerror:
                self.generator.addError("Bound Error") #print error
                self.generator.addExpAsign(tvalor,right="0")#tvalor = 0
                self.generator.addLabel(lsalida)
                if symbol.value.profundidad == len(self.cIndex):
                    result.tipo_aux = symbol.tipo
                elif symbol.value.profundidad > len(self.cIndex):
                    result.prof_array = symbol.value.profundidad - len(self.cIndex)
                    if symbol.tsimbolo == Symbols.VECTOR:
                        result.tipo_aux = Tipos.VECTOR

                    else:
                        result.tipo_aux = Tipos.ARREGLO
        else:
            error="No existe vector o arreglo con dicho id"
            print(error)
        return result