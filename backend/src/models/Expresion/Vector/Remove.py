from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.Driver import Driver
from models.TablaSymbols.Symbol import Symbols
from models.TablaSymbols.Tipos import Tipos
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.Symbol import Symbol
from models.TablaSymbols.ValC3d import ValC3d

class Remove(Expresion):
    def __init__(self, id: str, index: Expresion, line: int, column: int):
        super().__init__()
        self.value=None
        self.tipo=None
        self.id = id
        self.index = index
        self.line = line
        self.column = column
        self.instancia=0


    def ejecutar(self, driver: Driver, ts: Enviroment):
        self.getTipo(driver,ts)
        self.getValor(driver,ts);
    def getValor(self, driver, ts):
        self.instancia+=1
        if self.value==self.tipo==None:
            symbol = ts.buscar(self.id)
            t_index = self.index.getTipo(driver, ts)
            v_index = self.index.getValor(driver, ts)
            if symbol != None:  # si existe el vector, si ya fue declarado
                if symbol.mut == True:
                    if symbol.tsimbolo == Symbols.VECTOR:  # si lo que se llamo fue un vector
                        if t_index == Tipos.INT64 or t_index==Tipos.USIZE:  # el index es un entero
                            vector = symbol.value
                            self.value=vector.remove(v_index)

                            if self.value!=None:
                                self.tipo=symbol.tipo
                            else:
                                self.tipo=Tipos.ERROR
                        else:
                            print(f"El index debe de ser un entero linea: {self.line}")
                            error = "El index debe de ser un entero linea"
                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                              columna=self.column)
                    else:
                        print(f"Error Intento de Insert en una variable no vectorial  linea:{self.line} ")
                        error = "Error Intento de Insert en una variable no vectorial"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                          columna=self.column)
                else:
                    print(f"Intento de Insert en vector no muteable linea: {self.line}")
                    error = "Intento de Insert en vector no muteable"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
            else:
                print(f"Error Intento de Insert en vector no declarado linea:{self.line} ")
                error = "Error Intento de Insert en vector no declarado"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        return self.value

    def getTipo(self, driver, ts):
        self.resetInst()
        if self.value==self.tipo==None:
            self.getValor(driver,ts)
        else:
            self.instancia+=1
        return self.tipo
    def resetInst(self):
        if self.instancia>1:
            self.instancia=0
            self.value=None
            self.tipo=None

    def generarC3d(self,ts,ptr):
        self.generator.addComment(f"Remove en Vector {self.id}")
        tmpR=self.generator.newTemp()
        result=ValC3d(valor=tmpR,isTemp=True,tipo=Tipos.ERROR)
        auxStack = self.generator.newTemp()
        symbol: Symbol = ts.buscarC3d(self.id, auxStack,self.en_funcion)
        if symbol != None:
            if symbol.mut == True:
                if symbol.tsimbolo == Symbols.VECTOR:
                    self.index.generator = self.generator
                    indexR: ValC3d = self.index.generarC3d(ts, ptr)
                    if indexR.tipo in [Tipos.INT64, Tipos.USIZE]:
                        result.tipo=symbol.tipo
                        if symbol.value.profundidad==1:
                            result.tipo_aux=symbol.tipo
                        else:
                            result.tipo_aux=Tipos.ARREGLO
                        t_puntero = self.generator.newTemp()
                        t_tam = self.generator.newTemp()
                        t_tamNew = self.generator.newTemp()
                        t_aux = self.generator.newTemp()
                        t_capacity = self.generator.newTemp()
                        tcont = self.generator.newTemp()
                        loop = self.generator.newLabel()
                        loopAR = self.generator.newLabel()
                        lsalida = self.generator.newLabel()
                        lremove = self.generator.newLabel()
                        lerror = self.generator.newLabel()
                        t_indexRemove = self.generator.newTemp()

                        self.generator.addExpAsign(target=t_indexRemove, right=indexR.valor)

                        self.generator.addIf(left=t_indexRemove, rigth="0", operator="<",
                                             label=lerror)  # if ( tindexa<0 ) goto Lerror

                        self.generator.addBackStack(auxStack)
                        auxIndex = self.generator.newTemp()
                        self.generator.addExpression(target=auxIndex, left="P", right=str(symbol.position),
                                                     operator="+")
                        self.generator.addGetStack(target=t_puntero, index=auxIndex)
                        self.generator.addNextStack(auxStack)
                        self.generator.addGetHeap(target=t_tam, index=t_puntero)  # t_tam=inicioArray
                        self.generator.incVar(t_puntero)  # tpuntero=tpuntero+1
                        # CAPACITY
                        self.generator.addGetHeap(target=t_capacity, index=t_puntero)
                        self.generator.incVar(t_puntero)  # tpuntero=tpuntero+1


                        self.generator.addIf(left=t_indexRemove, rigth=t_tam, operator=">=",
                                             label=lerror)  # if (tindex>=tam) goto Lerror #Bounds Error

                        # INICIO Y NUEVO TAMAÑO DEL NUEVO ARREGLO:
                        self.generator.addExpAsign(target=tcont, right="0")  # tcont=0
                        # puntero del array ahora en una nueva posicion
                        self.generator.addSetStack(index=auxIndex, value="H")  # ahora el puntero anterior apunta
                        # al nuevo array
                        self.generator.addExpression(target=t_tamNew, left=t_tam, right="1",
                                                     operator="-")  # tamnew=tam+1
                        self.generator.addSetHeap(index="H", value=t_tamNew)  # Heap[H]=tamnew;
                        # nuevo tamaño del nuevo array
                        self.generator.addNextHeap()  # H=H+1
                        # CAPACITY
                        self.generator.addComment("New Capacity")
                        self.generator.addSetHeap(index="H", value=t_capacity)
                        self.generator.addNextHeap()  # H=H+1

                        # LOOP 1:
                        self.generator.addLabel(loopAR)  # LoopAI:                          loop antes del remove
                        self.generator.addIf(left=tcont, rigth=t_indexRemove, operator=">=",
                                             label=lremove)  # if (tcont >= tindex) goto Linsert
                        self.generator.addGetHeap(target=t_aux, index=t_puntero)
                        self.generator.addSetHeap(index="H", value=t_aux)
                        self.generator.incVar(t_puntero)
                        self.generator.incVar(tcont)
                        self.generator.addNextHeap()
                        self.generator.addGoto(loopAR)
                        # LREMOVE:
                        self.generator.addLabel(lremove)  # Linsert:
                        self.generator.addGetHeap(target=tmpR,index=t_puntero)
                        self.generator.incVar(t_puntero)
                        self.generator.incVar(tcont)
                        # LOOP 2:
                        # se copia el resto del contenido del array principal a una nueva posicion
                        self.generator.addLabel(loop)  # loop:
                        self.generator.addIf(left=tcont, rigth=t_tam, operator=">=",
                                             label=lsalida)  # if (tcont>=t_tam) goto Lsalida
                        self.generator.addGetHeap(target=t_aux, index=t_puntero)  # taux=Heap[t_index]
                        self.generator.addSetHeap(index="H", value=t_aux)  # Heap[H]=taux
                        self.generator.addNextHeap()  # H=H+1
                        self.generator.incVar(t_puntero)  # t_index=t_index+1
                        self.generator.incVar(tcont)  # tcont= tcont+1
                        self.generator.addGoto(loop)

                        self.generator.addLabel(lerror)
                        self.generator.addError("Bounds Error")
                        self.generator.addExpAsign(target=tmpR,right="0")
                        self.generator.addLabel(lsalida)
                    else:
                        error = "El index no es un int o usize"
                        print(error)
                else:
                    error = "Se intenta hacer push a una variable que no es un vector"
                    print(error)
            else:
                error = "Intento de cambio a un arreglo no muteable"
                print(error)
        else:
            error = "No existe dicho arreglo"
            print(error)
        self.generator.addComment("End remove")
        return result