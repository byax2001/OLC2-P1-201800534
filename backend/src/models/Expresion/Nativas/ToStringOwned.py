from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
from  models.TablaSymbols.ValC3d import ValC3d

class ToStringOwned(Expresion):
    def __init__(self,exp:Expresion,line:int,column:int):
        self.exp=exp
        self.line=line
        self.column=column
    def getValor(self, driver, ts):
        return str(self.exp.getValor(driver,ts))
    def getTipo(self, driver, ts):
        return Tipos.STRING
        # o solo simplemente return Tipos.STRING
    def ejecutar(self,driver,ts):
        pass
    def generarC3d(self,ts,ptr:int):
        self.exp.generator=self.generator
        self.generator.addComment("Metodo ToString o ToOwned")
        # ----------------------SOLO USADO EN EL CASO QUE LA EXPRESION SEA UN BOOLEANO
        tbool_str = self.generator.newTemp()  # contendra el indice donde inicia el booleano pasado a string
        self.generator.addExpAsign(target=tbool_str, right="H")
        # ----------------------------------------------------
        exp=self.exp.generarC3d(ts,ptr)
        newTemp=self.generator.newTemp()
        if exp.tipo == Tipos.STR or exp.tipo == Tipos.CHAR:
            self.generator.addExpAsign(target=newTemp,right=exp.valor)
            return ValC3d(valor=newTemp,isTemp=True,tipo=Tipos.STRING)
        elif exp.tipo==Tipos.BOOLEAN:
            self.addCopyStr(exp)
            self.generator.addSetHeap(index="H", value="-1")  # Heap[H]=-1
            self.generator.addNextHeap()  # H=H+1
            return ValC3d(valor=tbool_str, isTemp=True, tipo=Tipos.STRING)
        else:
            newTemp = self.generator.newTemp()  # = tnum
            self.generator.addExpAsign(target=newTemp,right="H")
            self.addCopyStr(exp)
            self.generator.addSetHeap(index="H",value="-1")  #Heap[H]=-1
            self.generator.addNextHeap() #H=H+1
            return ValC3d(valor=newTemp, isTemp=True, tipo=Tipos.STRING)

    def addCopyStr(self, exp: ValC3d):
        if exp.tipo_aux != Tipos.ARREGLO:
            if exp.tipo in [Tipos.INT64, Tipos.USIZE]:
                self.generator.addComment("Int o Usize to String")
                t1 = self.generator.newTemp()
                self.generator.addExpAsign(target=t1, right=exp.valor)
                self.setHeapStrNum(t1)
            elif exp.tipo==Tipos.FLOAT64:
                self.generator.addComment("Float to String")
                t1 = self.generator.newTemp()
                t2 = self.generator.newTemp()
                t3 = self.generator.newTemp()
                t4 = self.generator.newTemp()
                self.generator.addExpAsign(target=t1, right=exp.valor)  # t1 = 1245.552
                self.generator.addExpAsign(target=t2, right=f"(int){t1}")  # t2 = (int)t1
                self.generator.addExpression(target=t3, left=t1, right=t2, operator="-")  # t3=t1-t2
                self.generator.addExpression(target=t3, left=t3, right="1000000", operator="*")  # t3=t1-t2
                self.generator.addExpAsign(target=t4, right=f"round({t3})")
                self.setHeapStrNum(t2)  #parte entera
                self.generator.addSetHeap(index="H", value=str(ord(".")))  #punto
                self.generator.addNextHeap()  #parte decimal
                self.setHeapStrNum(t4)
            elif exp.tipo == Tipos.BOOLEAN:
                self.generator.addComment("Boolean to string")
                newLabel = self.generator.newLabel()  # Lsalida
                self.generator.addLabel(exp.trueLabel)  # añade Ln:  ya existente al codigo principal (true)
                self.generator.addSetHeap(index="H", value=str(ord("t")))
                self.generator.addNextHeap()
                self.generator.addSetHeap(index="H", value=str(ord("r")))
                self.generator.addNextHeap()
                self.generator.addSetHeap(index="H", value=str(ord("u")))
                self.generator.addNextHeap()
                self.generator.addSetHeap(index="H", value=str(ord("e")))
                self.generator.addNextHeap()
                self.generator.addGoto(newLabel)  # goto Lsalida;
                self.generator.addLabel(exp.falseLabel)  # añade Ln:  ya existente al codigo principal (false)
                self.generator.addSetHeap(index="H", value=str(ord("f")))
                self.generator.addNextHeap()
                self.generator.addSetHeap(index="H", value=str(ord("a")))
                self.generator.addNextHeap()
                self.generator.addSetHeap(index="H", value=str(ord("l")))
                self.generator.addNextHeap()
                self.generator.addSetHeap(index="H", value=str(ord("s")))
                self.generator.addNextHeap()
                self.generator.addSetHeap(index="H", value=str(ord("e")))
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
        self.generator.addIf(left=t1,rigth=t2,operator=">=",label=lsalida)# if t1>=t2 goto Lsalida
        self.generator.addGetHeap(target=t3,index=t2)#t3=Heap[t2]
        self.generator.addGetHeap(target=t4,index=t1)#t4=Heap[t1]
        self.generator.addSetHeap(index=t1,value=t3)#Heap[t1]=t3
        self.generator.addSetHeap(index=t2, value=t4)#Heap[t2]=t4
        self.generator.addExpression(target=t1,left=t1,right="1",operator="+")#t1=t1+1
        self.generator.addExpression(target=t2, left=t2, right="1", operator="-")#t2=t2-1
        self.generator.addGoto(loop)#goto Loop
        self.generator.addLabel(lsalida)#Lsalida:

