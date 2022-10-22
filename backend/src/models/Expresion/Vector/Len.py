from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import definirTipo
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d
from models.TablaSymbols.Symbol import Symbol,Symbols
from models.TablaSymbols.Tipos import Tipos

class Len(Expresion):
    def __init__(self,id:str,exp:Expresion,line:int,column:int,cIndex=[]):
        super().__init__()
        self.id=id
        self.value=None
        self.tipo=None
        self.exp = exp
        self.cIndexs=cIndex
        self.line=line
        self.column=column

    def ejecutar(self,driver,ts):
        pass
    def getValor(self, driver, ts):
        t_valor = self.exp.getTipo(driver, ts)
        valor=self.exp.getValor(driver,ts)
        if type(valor)==list or type(valor)==str:
            self.value=len(valor)
        else:
            print("Atributo no posee metodo len")
            error = "Atributo no posee metodo len"
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
        return self.value
    def getTipo(self, driver, ts):
        self.tipo=definirTipo(self.getValor(driver,ts))
        return self.tipo

    def generarC3d(self,ts,ptr):
        self.generator.addComment(f"Len de Vector {self.id}")
        tmpR=self.generator.newTemp()
        result=ValC3d(valor=tmpR,isTemp=True,tipo=Tipos.ERROR)
        auxStack = self.generator.newTemp()
        symbol: Symbol = ts.buscarC3d(self.id, auxStack,self.en_funcion)
        if symbol != None:
            if symbol.tsimbolo == Symbols.VECTOR or symbol.tsimbolo == Symbols.ARREGLO:
                t_tam = self.generator.newTemp()
                lerror = self.generator.newLabel()
                tvalor = self.generator.newTemp()
                taux = self.generator.newTemp()
                result.tipo = Tipos.INT64
                result.tipo_aux = Tipos.INT64
                t_puntero = self.generator.newTemp()
                lsalida = self.generator.newLabel()
                self.generator.addBackStack(auxStack)
                auxIndex = self.generator.newTemp()
                self.generator.addExpression(target=auxIndex, left="P", right=str(symbol.position),
                                             operator="+")
                self.generator.addNextStack(auxStack)
                self.generator.addGetStack(target=t_puntero, index=auxIndex)
                if symbol.paso_parametro: #si fue declarado como paso de parametro en el anterior puntero esta la direccion del verdadero array
                                          # ubicado en el stack
                    self.generator.addGetStack(target=t_puntero, index=t_puntero)
                if len(self.cIndexs) != 0:

                    if symbol.value.profundidad > len(self.cIndexs):
                        self.generator.addGetHeap(target=t_tam,index=t_puntero);
                        self.generator.addComment("Para saltarse la casilla del tamanio")
                        self.generator.incVar(t_puntero)
                        if symbol.tsimbolo == Symbols.VECTOR:
                            self.generator.addComment("Para saltarse el capacity")
                            self.generator.incVar(t_puntero);
                        x=0
                        for index in self.cIndexs:
                            x+=1
                            index.generator=self.generator
                            indexR : ValC3d = index.generarC3d(ts,ptr)
                            self.generator.addIf(left=indexR.valor,rigth=t_tam,operator=">=",label=lerror)
                            self.generator.addIf(left=indexR.valor, rigth="0", operator="<", label=lerror)
                            self.generator.addExpression(target=taux,left=t_puntero,right=indexR.valor,operator="+")#taux= tpuntero + index
                            #taux tiene la direccion del heap que tiene el inicio del subarray
                            self.generator.addGetHeap(target=tvalor,index=taux) #tvalor = Heap[taux] direccion del subarray
                            # TAMAÑO DEL SUBARRAY
                            self.generator.addComment("tvalor a retornar")
                            self.generator.addGetHeap(target=tmpR, index=tvalor)
                            if x!=len(self.cIndexs):
                                self.generator.addExpAsign(target=t_puntero,right=tvalor) #tpuntero = tvalor
                                self.generator.addComment("Tamanio")
                                self.generator.addGetHeap(target=t_tam,index=t_puntero) # t_tam = Heap[tpuntero]
                                self.generator.incVar(t_puntero) # tpuntero = tpuntero +1
                                if symbol.tsimbolo == Symbols.VECTOR:
                                    self.generator.incVar(t_puntero)
                        self.generator.addGoto(lsalida)  # goto Lsalida;
                        # EN CASO LOS INDEX DEN ERROR:
                        self.generator.addLabel(lerror)  # Lerror:
                        self.generator.addError("Bound Error")  # print error
                        self.generator.addExpAsign(tmpR, right="0")  # tvalor = 0
                        self.generator.addLabel(lsalida)
                    else:
                        error = "Se intenta usar len en un elemento que no es vector o arreglo en el interior de un arreglo "
                        print(error)
                else:
                    self.generator.addGetHeap(target=tmpR, index=t_puntero)  # t_tam=inicioArray
            elif symbol.tipo == Tipos.STRING:
                print() #por si acaso es necesario saber el tamaño de un string
            else:
                error = "Se intenta usar len en un elemento no vector o arreglo"
                print(error)
        else:
            error = "No existe dicho arreglo"
            print(error)
        self.generator.addComment("End Len")
        return result