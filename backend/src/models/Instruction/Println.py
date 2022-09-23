from models.Abstract.Instruction import Instruccion
from models.Abstract.Expresion import Expresion
from models.Expresion.Primitivo import Primitivo
from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Symbol import Symbols
from models.Expresion.Id import Id
#VECTORES Y ARRAYS
from models.Expresion.Vector.vecI import vecI
from models.Expresion.Arreglo.Arreglo import Arreglo
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d

class Println(Instruccion):

    def __init__(self, exp: Expresion,cExp:[Expresion], linea, columna):
        self.columna = columna
        self.linea = linea
        self.exp = exp
        self.cExp=cExp

    def ejecutar(self, driver, ts):
        if len(self.cExp)==0:
            if isinstance(self.exp,Primitivo):
                driver.append(str(self.exp.getValor(driver, ts))+"\n")
            else:
                print("Error: forma incorrecta de imprimir")
                error = "Error: forma incorrecta de imprimir"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                  columna=self.columna)
        else:
            #Conteo de {} y {:?} presentes en la variable auxiliar
            c_llaves=0   #llaves necesarias para imprimir
            c_llavesint=0  #para imprimir arrays enteros
            for element in self.cExp:
                if isinstance(element,Id):
                    Symbol=element.getSymbol(driver,ts) #este metodo se encuentra declarado en la clase Id.py
                    if Symbol != None:
                        if Symbol.tsimbolo == Symbols.VARIABLE:
                            c_llaves+=1
                        elif Symbol.tsimbolo == Symbols.ARREGLO or Symbol.tsimbolo == Symbols.VECTOR:
                            c_llavesint+=1
                        elif Symbol.tsimbolo == Symbols.FUNCION:
                            print("Se debe de ejecutar la funcion y no solo colocar id")
                            error = "Se debe de ejecutar la funcion y no solo colocar id"
                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                              columna=self.columna)
                            return
                    else:
                        print("Error una de las expresiones a imprimir es un id no declarado")
                        error = "Error una de las expresiones a imprimir es un id no declarado"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                          columna=self.columna)
                        return
                elif isinstance(element,vecI) or isinstance(element,Arreglo):
                    c_llavesint+=1;
                elif isinstance(element,Primitivo):
                    c_llaves+=1

            #reemplazo de los {} y {:?} por las expresiones en la cadena auxiliar, arriba se cubrieron todos los posibles errores, por lo cual no es necesario volver a cubrirlos
            #replace (exp1,exp2,1) indica que solo se reemplazara una vez de izquierda a derecha
            if self.exp.getTipo(driver,ts) == Tipos.STR: #<--------expresion auxiliar "{}  {:?}"
                v_exp=str(self.exp.getValor(driver,ts))
                if v_exp.count("{}")==c_llaves and v_exp.count("{:?}")==c_llavesint:
                    for exp in self.cExp: #se procede a recorrer cada expresion
                        valorCexp = exp.getValor(driver, ts)
                        t_valorCexp=exp.getTipo(driver,ts)
                                    #el getvalor de un id que es vector o arreglo devuelve el vector contenido en la clase VECTOR por un metodo en la clase ID.py
                        if isinstance(exp, Id):  #si la expresion es un id, hay que analizar si es un arreglo o una variable
                            Symbol = exp.getSymbol(driver, ts)
                            if Symbol.tsimbolo == Symbols.VARIABLE:
                                v_exp=v_exp.replace("{}",str(valorCexp),1)  #si es una variable normal se reemplaza de forma comun
                            elif Symbol.tsimbolo == Symbols.ARREGLO or Symbol.tsimbolo == Symbols.VECTOR:
                                valorCexp=self.printArray(valorCexp); #metodo para imprimir un array correctamente
                                v_exp=v_exp.replace("{:?}",valorCexp,1) #si es un arreglo se reemplza {:?} por el arreglo
                        elif type(valorCexp)==list: #si el valor a imprimir es un array
                            valorCexp = self.printArray(valorCexp)
                            v_exp = v_exp.replace("{:?}", valorCexp, 1)
                        else:
                            v_exp=v_exp.replace("{}",str(valorCexp),1) #si es un primitivo u otro dato se reemplaza de forma comun
                    driver.append(v_exp+"\n") #se copia a la consola la cadena resultante
                else:
                    for element in self.cExp:

                        tipo = element.getTipo(driver, ts)
                        valor = element.getValor(driver, ts)
                        if type(valor) == list:
                            valor=self.printArray(valor)
                            v_exp = v_exp.replace("{:?}", str(valor), 1)
                        else:
                            v_exp = v_exp.replace("{}", str(valor), 1)
                    if v_exp.count("{}")==0 and v_exp.count("{:?}")==0:
                        driver.append(str(v_exp) + "\n")
                    else:
                        print("Error la expresion auxiliar no tiene la cantidad adecuada de {} y/o {:?}")
                        error = "Error la expresion auxiliar no tiene la cantidad adecuada de {} y/o {:?}"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                          columna=self.columna)
            else:
                print("Error la expresion auxiliar para imprimir variables no es string")
                error = "Error la expresion auxiliar para imprimir variables no es string"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                  columna=self.columna)
    def printArray(self,arrayVec):
        vector="["
        if type(arrayVec)==list:
            for x in range(len(arrayVec)):
                v_element = arrayVec[x]["valor"]
                if type(v_element)==list:
                    v_element=self.printArray(v_element)
                if x!=(len(arrayVec)-1):
                    vector=vector+str(v_element)+","
                else:
                    vector=vector+str(v_element)+"]"
            if len(arrayVec)==0:
                vector=vector+"]"
        return vector

    def generarC3d(self,ts,ptr:int):
        if len(self.cExp) == 0:
            if isinstance(self.exp, Primitivo):
                self.exp.generator=self.generator
                exp=self.exp.generarC3d(ts,ptr)
                if exp.tipo in [Tipos.STR,Tipos.STRING,Tipos.CHAR]:
                    self.generator.addComment("Print de un String o CHAR")
                    self.printCadenaC3d(posInit=exp.valor)
                elif exp.tipo in [Tipos.INT64,Tipos.USIZE]:
                    self.generator.addComment("Print de un Int o Usize")
                    self.generator.addPrintf(typePrint="d", value=exp.valor)
                elif exp.tipo==Tipos.FLOAT64:
                    self.generator.addComment("Print de un Float")
                    self.generator.addPrintf(typePrint="f", value=exp.valor)
                elif exp.tipo== Tipos.BOOLEAN:
                    self.generator.addComment("Print de un Boolean")
                    newLabel = self.generator.newLabel()  #Lsalida
                    self.generator.addLabel(exp.trueLabel)  # añade Ln:  ya existente al codigo principal (true)
                    self.generator.addPrintf(typePrint="c",value=ord("t"))
                    self.generator.addPrintf(typePrint="c", value=ord("r"))
                    self.generator.addPrintf(typePrint="c", value=ord("u"))
                    self.generator.addPrintf(typePrint="c", value=ord("e"))
                    self.generator.addGoto(newLabel)  # goto Lsalida;
                    self.generator.addLabel(exp.falseLabel)  # añade Ln:  ya existente al codigo principal (false)
                    self.generator.addPrintf(typePrint="c", value=ord("f"))
                    self.generator.addPrintf(typePrint="c", value=ord("a"))
                    self.generator.addPrintf(typePrint="c", value=ord("l"))
                    self.generator.addPrintf(typePrint="c", value=ord("s"))
                    self.generator.addPrintf(typePrint="c", value=ord("e"))
                    self.generator.addLabel(newLabel)  # Lsalida:
            else:
                error = "Error: forma incorrecta de imprimir"
                print(error)
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                  columna=self.columna)
        else:
            self.generator.addComment("Instruccion Print")
            self.exp.generator=self.generator
            print_aux=self.exp.generarC3d(ts,ptr)    #println!("{}",var)   "{}"=printaux
            taux=self.generator.newTemp()
            #a cada una de las expresiones un exp.generator=self.generator
            for exp in self.cExp:
                exp.generator=self.generator
                c3d_exp = exp.generarC3d(ts, ptr)
                self.generator.addComment("Para saber donde iniciar a imprimir luego del proceso")
                self.generator.addExpAsign(target=taux, right="H")
                contador=self.generator.newTemp() #t1
                texp=self.generator.newTemp() #texp
                loop=self.generator.newLabel()
                loop2=self.generator.newLabel()
                loop4=self.generator.newLabel()
                Lv1=self.generator.newLabel()
                Lf1=self.generator.newLabel()
                Lsalida=self.generator.newLabel()
                llavea=str(ord("{")) #ya pasados a ascii
                llavec=str(ord("}"))
                self.generator.addComment("Print Complex P.1")
                self.generator.addExpression(target=contador,left=str(print_aux.valor),right="",operator="") #t1=init1
                self.generator.addLabel(loop) #Loop:
                self.generator.addGetHeap(target=texp,index=contador) # texp=Heap[contador]
                self.generator.addIf(left=texp,rigth=f"(char){llavea}",operator="==",label=Lv1) #if (texp=="{") goto Lv1
                self.generator.addSetHeap(index="H",value=texp) #Heap[H]=texp
                self.generator.addNextHeap()#H=H+1
                self.generator.addExpression(target=contador,left=contador,right="1",operator="+") #cont=cont+1
                self.generator.addGoto(loop) # goto Loop

                self.generator.addComment("Print Complex P.2")
                self.generator.addLabel(Lv1) #Lv1:
                self.generator.addExpression(target=contador, left=contador, right="1", operator="+") #para saltarse el "{" de la exp aux
                self.generator.addLabel(loop2) #loop2:
                self.generator.addGetHeap(target=texp,index=contador) # texp=Heap[contador]
                self.generator.addIf(left=texp,rigth=f"(char){llavec}",operator="==",label=Lf1)
                self.generator.addExpression(target=contador, left=contador, right="1", operator="+")  # cont=cont+1
                self.generator.addGoto(loop2) #goto loop2
                self.generator.addComment("Print Complex P.3")
                self.generator.addLabel(Lf1) #Lf1:
                self.generator.addExpression(target=contador, left=contador, right="1", operator="+")#para saltarse el "}" de la exp_aux
                self.addCopyStr(exp=c3d_exp)  #metodo para sustituir un {} o {:?} por una variable
                self.generator.addComment("Print Complex P.4")
                self.generator.addLabel(loop4)  # Loop4:
                self.generator.addGetHeap(target=texp, index=contador)  # texp=Heap[contador]
                self.generator.addIf(left=texp, rigth=f"-1", operator="==",
                                     label=Lsalida)  # if (texp=="{") goto Lv1
                self.generator.addSetHeap(index="H", value=texp)  # Heap[H]=texp
                self.generator.addNextHeap()  # H=H+1
                self.generator.addExpression(target=contador, left=contador, right="1", operator="+")  # cont=cont+1
                self.generator.addGoto(loop4)  # goto Loop


                self.generator.addComment("Salida print Complex")
                self.generator.addLabel(Lsalida) #Lsalida:
                self.generator.addSetHeap(index="H", value="-1")  # Heap[H]=-1
                self.generator.addNextHeap()  # H=H+1
                print_aux.valor=taux   #para que contador ahora inicie desde la nueva cadena formada:
                                       #primera iteracion de "{}--{}","hola,"quetal" :   "hola"--{}
                taux=self.generator.newTemp()
                #self.generator.addExpAsign(target=contador,right="H")
            self.generator.addComment("Impresion")
            self.printCadenaC3d(posInit=print_aux.valor)



    def printCadenaC3d(self,posInit:str):
        contador = self.generator.newTemp()
        self.generator.addExpression(target=contador, left=posInit, right="", operator="")  # Contador = posInit;
        loop = self.generator.newLabel()  # Loop
        self.trueLabel = self.generator.newLabel()  # Lv
        self.falseLabel = self.generator.newLabel()  # LF

        self.generator.addLabel(loop)  # Loop:
        texp = self.generator.newTemp()  # texp
        self.generator.addGetHeap(texp, contador)  # texp = Heap[contador];
        self.generator.addIf(left=texp, rigth="-1", operator="!=", label=self.trueLabel)  # if (texp!=-1) goto Lv
        self.generator.addGoto(self.falseLabel)  # goto Lf
        self.generator.addLabel(self.trueLabel)  # Lv:
        self.generator.addPrintf(typePrint="c",value=f"(char){texp}")  #funcionaria con (char) o con (int)
        self.generator.addExpression(target=contador, left=contador, right="1", operator="+")  # contador=contador+1;
        self.generator.addGoto(loop)  # goto Loop
        self.generator.addLabel(self.falseLabel)  # Lf:

        # copia un string o un valor de una posicion al H libre mas actual como otro string
    #copiar el valor de una expresion en la pila
    def addCopyStr(self, exp: ValC3d):
        if exp.tipo != Tipos.ARREGLO:
            if exp.tipo in [Tipos.STR, Tipos.STRING, Tipos.CHAR]:
                contador = self.generator.newTemp()

                self.generator.addExpression(target=contador, left=exp.valor, right="",
                                             operator="")  # Contador = posInit;
                loop = self.generator.newLabel()  # Loop
                Lf = self.generator.newLabel()  # LF

                self.generator.addLabel(loop)  # Loop:
                texp = self.generator.newTemp()  # texp
                self.generator.addGetHeap(texp, contador)  # texp = Heap[contador];
                self.generator.addIf(left=texp, rigth="-1", operator="==", label=Lf)  # if (texp==-1) goto Lf
                self.generator.addSetHeap("H", texp)  # Heap[H]=texp
                self.generator.addNextHeap()  # H=H+1
                self.generator.addExpression(target=contador, left=contador, right="1",
                                             operator="+")  # contador=contador+1;
                self.generator.addGoto(loop)  # goto Loop
                self.generator.addLabel(Lf)  # Lf:
            elif exp.tipo in [Tipos.INT64, Tipos.USIZE]:
                self.generator.addComment("Num to String")
                t1 = self.generator.newTemp()
                self.generator.addExpAsign(target=t1, right=exp.valor)
                self.setHeapStrNum(t1)
            elif exp.tipo==Tipos.FLOAT64:
                t1 = self.generator.newTemp()
                t2 = self.generator.newTemp()
                t3 = self.generator.newTemp()
                t4 = self.generator.newTemp()
                self.generator.addExpAsign(target=t1, right=exp.valor)  # t1 = 1245.552
                self.generator.addExpAsign(target=t2, right=f"(int){t1}")  # t2 = (int)t1
                self.generator.addExpression(target=t3, left=t1, right=t2, operator="-")  # t3=t1-t2
                self.generator.addExpression(target=t3, left=t3, right="1000000", operator="*")  # t3=t1-t2
                self.generator.addExpAsign(target=t4, right=f"round({t3})")
                self.setHeapStrNum(t2)
                self.generator.addSetHeap(index="H", value=str(ord(".")))
                self.generator.addNextHeap()
                self.setHeapStrNum(t4)
            elif exp.tipo == Tipos.BOOLEAN:
                self.generator.addComment("Print de un Boolean")
                newLabel = self.generator.newLabel()  # Lsalida
                self.generator.addLabel(exp.trueLabel)  # añade Ln:  ya existente al codigo principal (true)
                self.generator.addSetHeap(index="H", value=ord("t"))
                self.generator.addNextHeap()
                self.generator.addSetHeap(index="H", value=ord("r"))
                self.generator.addNextHeap()
                self.generator.addSetHeap(index="H", value=ord("u"))
                self.generator.addNextHeap()
                self.generator.addSetHeap(index="H", value=ord("e"))
                self.generator.addNextHeap()
                self.generator.addGoto(newLabel)  # goto Lsalida;
                self.generator.addLabel(exp.falseLabel)  # añade Ln:  ya existente al codigo principal (false)
                self.generator.addSetHeap(index="H", value=ord("f"))
                self.generator.addNextHeap()
                self.generator.addSetHeap(index="H", value=ord("a"))
                self.generator.addNextHeap()
                self.generator.addSetHeap(index="H", value=ord("l"))
                self.generator.addNextHeap()
                self.generator.addSetHeap(index="H", value=ord("s"))
                self.generator.addNextHeap()
                self.generator.addSetHeap(index="H", value=ord("e"))
                self.generator.addNextHeap()
                self.generator.addLabel(newLabel)  # Lsalida:
    #pasar un numero a string en c++
    def setHeapStrNum(self,tvalor):
        linit=self.generator.newTemp()
        t1=self.generator.newTemp()
        t2=self.generator.newTemp()
        t3=self.generator.newTemp()
        t4=self.generator.newTemp()
        loop=self.generator.newLabel()
        Lf=self.generator.newLabel()
        self.generator.addExpAsign(target=linit,right="H")#usado para el metodo de reordenar a la inversa
        self.generator.addExpression(target=t1,left=tvalor,right="",operator="") #t1=valor double o int
        self.generator.addLabel(loop) #Loop
        self.generator.addExpression(target=t2, left=t1, right="10", operator="/") #t2=t1/10
        self.generator.addExpAsign(target=t3, right=f"(int){t2}") #t3=(int)t2
        self.generator.addIf(left=t3,rigth="0",operator="==",label=Lf) #if(t3==0) goto Lf
        self.generator.addExpAsign(target=t4,right=f"fmod({t1},10)") # t4=fmod(t1,10):  t4=t1%10

        self.generator.addExpAsign(target=t1,right=t3) #t1=t3
        self.generator.addSetHeap(index="H",value=f"(int){t4} +48") #Heap[H]=(char)t4+48   #EN ASSEMBLER CUANDO SE LE SUMA 30h A UN NUMERO
                                                                                            #SE CONVIERTE A ASCII, EN ESTE CASO SE SUMAN 48
                                                                                            #POR QUE 48d==30h
        self.generator.addNextHeap() #H=H+1
        self.generator.addGoto(loop)
        self.generator.addLabel(Lf) # Lf:
        self.generator.addSetHeap(index="H", value=f"(int){t1}+48") #Heap[H]=(char)t4
        self.generator.addNextHeap()  # H=H+1
        self.sort_reverse(init=linit,fin="H-1")


    #metodo para colocar al reves un string en la pila
    def sort_reverse(self,init,fin):
        self.generator.addComment("sort_revers")
        t1=self.generator.newTemp()
        t2=self.generator.newTemp()
        t3=self.generator.newTemp()
        t4=self.generator.newTemp()
        loop=self.generator.newLabel()
        lsalida=self.generator.newLabel()
        self.generator.addExpAsign(target=t1,right=init) #t1=init
        self.generator.addExpAsign(target=t2, right=fin) #t2=finish
        self.generator.addLabel(loop) #Loop:
        self.generator.addIf(left=t1,rigth=t2,operator="==",label=lsalida)# if t1==t2 goto Lsalida
        self.generator.addIf(left=t1, rigth=t2, operator=">", label=lsalida)  # if t1>t2 goto Lsalida
        self.generator.addGetHeap(target=t3,index=t2)#t3=Heap[t2]
        self.generator.addGetHeap(target=t4,index=t1)#t4=Heap[t1]
        self.generator.addSetHeap(index=t1,value=t3)#Heap[t1]=t3
        self.generator.addSetHeap(index=t2, value=t4)#Heap[t2]=t4
        self.generator.addExpression(target=t1,left=t1,right="1",operator="+")#t1=t1+1
        self.generator.addExpression(target=t2, left=t2, right="1", operator="-")#t2=t2-1
        self.generator.addGoto(loop)#goto Loop
        self.generator.addLabel(lsalida)#Lsalida:

