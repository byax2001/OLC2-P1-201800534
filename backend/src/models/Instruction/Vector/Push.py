from models.Abstract.Instruction import Instruccion
from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Symbol import Symbols,Symbol
from models.Driver import Driver
from models.TablaSymbols.Enviroment import Enviroment
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d
class Push(Instruccion):
    def __init__(self,id:str,exp:Expresion,line:int,column:int):
        super().__init__()
        self.id=id
        self.exp=exp
        self.line=line
        self.column=column
    def ejecutar(self, driver: Driver, ts: Enviroment):
        symbol=ts.buscar(self.id)
        if symbol!=None:
            if symbol.mut==True:
                if symbol.tsimbolo==Symbols.VECTOR:
                    v_exp=self.exp.getValor(driver,ts)
                    t_exp=self.exp.getTipo(driver,ts)
                    if v_exp!=None and t_exp!=Tipos.ERROR:
                        if t_exp==symbol.tipo:
                            vector=symbol.value
                            vector.push({"valor":v_exp,"tipo":t_exp})
                        else:
                            print(f"Error Intento de push de un valor con un tipo distinto al vector linea:{self.line} ")
                            error = "Error Intento de push de un valor con un tipo distinto al vector"
                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                              columna=self.column)
                    else:
                        print(f"Expresion causa error al intentar hacer push  linea:{self.line} ")
                        error = "Expresion causa error al intentar hacer push "
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                          columna=self.column)
                else:
                    print(f"Error Intento de push en una variable no vectorial  linea:{self.line} ")
                    error = "Error Intento de push en una variable no vectorial "
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
            else:
                print(f"Intento de Push en vector no muteable linea: {self.line}")
                error = "Intento de Push en vector no muteable "
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        else:
            print(f"Error Intento de push en vector no declarado linea:{self.line} ")
            error = "Error Intento de push en vector no declarado "
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
    def generarC3d(self,ts:Enviroment,ptr):
        self.generator.addComment(f"Push Vector {self.id}")
        auxStack = self.generator.newTemp()
        symbol:Symbol = ts.buscarC3d(self.id,auxStack)
        if symbol != None:
            if symbol.mut == True:
                if symbol.tsimbolo==Symbols.VECTOR:
                    self.exp.generator=self.generator
                    expR:ValC3d=self.exp.generarC3d(ts,ptr)
                    if symbol.tipo == expR.tipo:
                        t_puntero = self.generator.newTemp()
                        t_tam = self.generator.newTemp()
                        t_capacity = self.generator.newTemp()
                        t_tamNew = self.generator.newTemp()
                        t_aux = self.generator.newTemp()
                        tcont = self.generator.newTemp()
                        loop = self.generator.newLabel()
                        lsalida = self.generator.newLabel()

                        self.generator.addBackStack(auxStack)
                        auxIndex=self.generator.newTemp()
                        self.generator.addExpression(target=auxIndex,left="P",right=str(symbol.position),operator="+")
                        self.generator.addNextStack(auxStack)
                        self.generator.addGetStack(target=t_puntero, index=auxIndex)
                        if symbol.paso_parametro:  # si fue declarado como paso de parametro en el anterior puntero esta la direccion del verdadero array
                            # ubicado en el stack
                            self.generator.addGetStack(target=t_puntero, index=t_puntero)
                        #TAMAÑO
                        self.generator.addGetHeap(target=t_tam,index=t_puntero)# t_tam=inicioArray
                        self.generator.incVar(t_puntero) #tpuntero=tpuntero+1
                        #CAPACITY
                        self.generator.addGetHeap(target=t_capacity,index=t_puntero)
                        #DUPLICAR CAPACIDAD DE VECTOR SI SE INGRESA UN ELEMENTO QUE HACE UN TAMAÑO MAYOR A LA CAPACIDAD
                        LnoDupCapacity=self.generator.newLabel()
                        capNot0 = self.generator.newLabel()
                        self.generator.addComment("Si la capacidad es 0")
                        self.generator.addIf(left=t_capacity, rigth="0", operator="!=", label=capNot0)
                        self.generator.addExpAsign(target=t_capacity, right="4")
                        self.generator.addLabel(capNot0)
                        self.generator.addComment("Si el tamanio es igual o mayor a capacity")
                        self.generator.addIf(left=t_tam,rigth=t_capacity,operator="<",label=LnoDupCapacity)
                        self.generator.addExpression(target=t_capacity,left=t_capacity,right="2",operator="*")
                        self.generator.addLabel(LnoDupCapacity)
                        self.generator.incVar(t_puntero)  # tpuntero=tpuntero+1

                        self.generator.addExpAsign(target=tcont,right="0")# tcont=0
                        #puntero del array ahora en una nueva posicion
                        self.generator.addSetStack(index=auxIndex,value="H")# ahora el puntero anterior apunta
                                                                            # al nuevo array
                        self.generator.addComment("New Tamanio")
                        self.generator.addExpression(target=t_tamNew,left=t_tam,right="1",operator="+") #tamnew=tam+1
                        self.generator.addSetHeap(index="H",value=t_tamNew)# Heap[H]=tamnew; //nuevo tamaño del nuevo array
                        self.generator.addNextHeap()# H=H+1
                        #CAPACITY
                        self.generator.addComment("New Capacity")
                        self.generator.addSetHeap(index="H", value=t_capacity)
                        self.generator.addNextHeap()  # H=H+1

                        # se copia el contenido del array principal a una nueva posicion
                        self.generator.addLabel(loop)# loop:
                        self.generator.addIf(left=tcont,rigth=t_tam,operator=">=",label=lsalida) #if (tcont>=t_tam) goto Lsalida
                        self.generator.addGetHeap(target=t_aux,index=t_puntero)#   taux=Heap[t_index]
                        self.generator.addSetHeap(index="H",value=t_aux)#   Heap[H]=taux
                        self.generator.addNextHeap()#   H=H+1
                        self.generator.incVar(t_puntero)#   t_index=t_index+1
                        self.generator.incVar(tcont)#   tcont= tcont+1
                        self.generator.addGoto(loop)# goto loop
                        self.generator.addLabel(lsalida)# Lsalida:
                        #se copia en la ultima posicion el nuevo valor
                        self.generator.addSetHeap(index="H",value=expR.valor)
                        self.generator.addNextHeap()#H=H+1
                    else:
                        error="La expresion y el arreglo no son del mismo tipo"
                        print(error)
                else:
                    error = "Se intenta hacer push a una variable que no es un vector"
                    print(error)
            else:
                error="Intento de cambio a un arreglo no muteable"
                print(error)
        else:
            error="No existe dicho arreglo"
            print(error)