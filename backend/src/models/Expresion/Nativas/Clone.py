from models.Abstract.Expresion import Expresion
from models.TablaSymbols.ValC3d import ValC3d
from models.TablaSymbols.Tipos import Tipos
from models.Expresion.Vector.AccesVec import AccesVec
from models.Expresion.Id import Id

class Clone(Expresion):
    def __init__(self,exp:Expresion,line:int,column:int):
        super().__init__()
        self.exp=exp
        self.line=line
        self.column=column
    def getValor(self, driver, ts):
        return self.exp.getValor(driver,ts)
    def getTipo(self, driver, ts):
        return self.exp.getTipo(driver,ts)
        # o solo simplemente return Tipos.STRING
    def ejecutar(self,driver,ts):
        pass
    def generarC3d(self,ts,ptr):
        self.generator.addComment("--Clone()--")
        self.exp.generator = self.generator
        exp:ValC3d = self.exp.generarC3d(ts,ptr)
        if exp.tipo_aux == Tipos.ARREGLO or exp.tipo_aux == Tipos.VECTOR:
            if not isinstance(self.exp,Id) and not isinstance(self.exp,AccesVec):
                exp.prof_array = exp.prof_array + 1
            self.generator.addComment("Puntero del nuevo array")
            tmpR = self.generator.newTemp()
            self.generator.addExpAsign(target=tmpR, right="H")
            exp.valor= tmpR
            exp.isTemp=True
        return exp

    def cloneArrays(self,exp:ValC3d):
        if exp.prof_array == 1:
            t_tam = self.generator.newTemp()
            t_puntero = self.generator.newTemp()
            loop = self.generator.newLabel()
            lsalida = self.generator.newLabel()
            t_cont = self.generator.newTemp()
            t_aux = self.generator.newTemp()
            t_valor = self.generator.newTemp()
            self.generator.addExpAsign(target=t_cont, right="0")
            self.generator.addExpAsign(target=t_puntero, right=exp.valor)
            self.generator.addGetHeap(target=t_tam, index=t_puntero)
            self.generator.incVar(t_tam)  # tomando en cuenta el espacio donde se aloja el tamaño del vector
            if exp.tipo_aux == Tipos.VECTOR:
                self.generator.incVar(t_tam)  # tomando en cuenta el espacio donde se aloja el capacity
            self.generator.addLabel(loop)  # LOOP:
            self.generator.addIf(left=t_cont, rigth=t_tam, operator=">=", label=lsalida)  # if tcont >= tam goto Lsalida
            self.generator.addExpression(target=t_aux, left=t_cont, right=t_puntero, operator="+")  # taux = tpuntero + cont
            self.generator.addGetHeap(target=t_valor, index=t_aux)  # tval = Heap[taux]
            self.generator.addSetHeap(index="H", value=t_valor)  # Heap[H] = tval
            self.generator.addNextHeap()  # H = H +1;
            self.generator.incVar(t_cont)  # tcont = tcont+1
            self.generator.addGoto(loop)  # Goto Loop
            self.generator.addLabel(lsalida)
        else:
            t_puntero = self.generator.newTemp()
            t_tam = self.generator.newTemp()
            loop1 = self.generator.newLabel()
            loop = self.generator.newTemp()
            lsalida1 = self.generator.newLabel()
            lsalida = self.generator.newLabel()
            t_IcA = self.generator.newTemp() #inicio del contenido del arreglo: [tamaño][capacity][contenido...]
            t_cont = self.generator.newTemp()
            taux2 = self.generator.newTemp()
            taux3 = self.generator.newTemp()
            tpunteroHijo = self.generator.newTemp()
            self.generator.addExpAsign(target=t_puntero,right=exp.valor)# tpuntero = tpuntero
            self.generator.addGetHeap(target=t_tam,index=t_puntero)# ttam = Heap[tpuntero]
            self.generator.addSetHeap(index="H",value=t_tam)# Heap[H] = ttam
            self.generator.addNextHeap()#H = H + 1
            self.generator.incVar(t_puntero)# tpuntero = tpuntero + 1;
            if exp.tipo_aux == Tipos.VECTOR:
                t_capacity = self.generator.newTemp()
                self.generator.addGetHeap(target=t_capacity,index=t_puntero)# tcapacity = Heap[tpuntero]
                self.generator.addSetHeap(index="H",value=t_capacity)# Heap[H] = tcapacity
                self.generator.incVar(t_puntero)# tpuntero = tpuntero +1
                self.generator.addNextHeap()# H= H+1

            self.generator.addExpAsign(target=t_IcA,right="H")# t_iCA = "H"
            self.generator.addExpAsign(target=t_cont,right="0")# tcont = 0

            self.generator.addLabel(loop1)# loop1:
            self.generator.addIf(left=t_cont,rigth=t_tam,operator=">=",label=lsalida1)# if ( tcont >= ttam ) goto Lsalida1
            self.generator.addNextHeap()#	H=H+1
            self.generator.incVar(t_cont)#  tcont = tcont+1
            self.generator.addGoto(loop1)# goto Loop1
            self.generator.addLabel(lsalida1)# Lsalida1:

            self.generator.addExpAsign(target=t_cont,right="0")# tcont = 0

            self.generator.addLabel(loop)# loop:
            self.generator.addIf(left=t_cont,rigth=t_tam,operator=">=",label=lsalida)# if ( tcont >= ttam ) goto Lsalida
            self.generator.addExpAsign(target=taux2,right="H")# taux2 = "H"
            self.generator.addExpression(target=taux3,left=t_puntero,right=t_cont,operator="+")# taux3 = tpuntero + tcont
            self.generator.addGetHeap(target=tpunteroHijo,index=taux3)# tpunteroHijo= Heap[taux3]
            expHijo = ValC3d(valor=tpunteroHijo,isTemp=True,tipo=exp.tipo,tipo_aux=exp.tipo_aux)# CopyArray(tpunteroHijo)
            expHijo.prof_array = exp.prof_array - 1
            self.cloneArrays(expHijo)
            self.generator.addSetHeap(index=t_IcA,value=taux2)# Heap[t_iCA] = taux2
            self.generator.incVar(t_IcA)# t_iCA = taux + 1
            self.generator.incVar(t_cont)# tcont = tcont +1;
            self.generator.addGoto(label=loop)# goto Loop
            self.generator.addLabel(lsalida)# Lsalida: