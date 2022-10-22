from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d

class Rango(Expresion):
    def __init__(self, exp1:Expresion,exp2:Expresion,line:int,column:int):
        super().__init__()
        self.value=None
        self.tipo=None
        self.exp1=exp1
        self.exp2=exp2
        self.line=line
        self.column=column
        self.instancia=0
    def getValor(self, driver, ts):
        self.instancia+=1
        if self.value==None and self.tipo==None:
            t_exp1 = self.exp1.getTipo(driver, ts)
            t_exp2 = self.exp2.getTipo(driver,ts)
            if t_exp1==Tipos.INT64 and t_exp2==Tipos.INT64:
                v_exp1=self.exp1.getValor(driver,ts)
                v_exp2=self.exp2.getValor(driver,ts)
                vector=[]
                for i in range(v_exp1,v_exp2):
                    vector.append({"valor":i,"tipo":Tipos.INT64})
                self.value=vector
                self.tipo=Tipos.INT64
            else:
                print("Uno o los dos parametros de rango no son enteros o causan conflictos")
                error = "Uno o los dos parametros de rango no son enteros o causan conflictos"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        return self.value
    def getTipo(self, driver, ts):
        self.resetInst()
        if self.tipo==None:
            self.getValor(driver,ts)
            if self.value==None:
                self.tipo==Tipos.ERROR
        else:
            self.instancia+=1
        return self.tipo
    def ejecutar(self,driver,ts):
        pass
    def resetInst(self):
        if self.instancia>1:
            self.instancia=0
            self.value=None
            self.tipo=None
    def generarC3d(self,ts,ptr):
        self.generator.addComment("RANGO")
        result = ValC3d(valor="0",isTemp=False,tipo=Tipos.ERROR)
        self.exp1.generator = self.generator
        self.exp2.generator = self.generator
        exp1:ValC3d = self.exp1.generarC3d(ts,ptr)
        exp2: ValC3d = self.exp2.generarC3d(ts,ptr)
        if exp1.tipo in [Tipos.INT64,Tipos.USIZE] and exp2.tipo in [Tipos.INT64,Tipos.USIZE]:
            v1 = self.generator.newTemp()
            v2 = self.generator.newTemp()
            t_cont = self.generator.newTemp()
            loop = self.generator.newLabel()
            lsalida = self.generator.newLabel()
            t1 = self.generator.newTemp()
            tmpR = self.generator.newTemp()

            self.generator.addExpAsign(target=v1,right=exp1.valor)
            self.generator.addExpAsign(target=v2,right=exp2.valor)
            self.generator.addExpAsign(target=t_cont,right="0")# tcont = 0
            self.generator.addExpAsign(target=tmpR, right="H")# tmpR = H
            self.generator.addNextHeap()# H = H + 1;
            self.generator.addLabel(loop)# Loop:
            self.generator.addIf(left=v1,rigth=v2,operator=">=",label=lsalida)#   if (t1 == -1 ) goto Lsalida
            self.generator.incVar(t_cont)#	tcont = tcont +1
            self.generator.addSetHeap(index="H",value=v1)#	Heap[H] = v1
            self.generator.addNextHeap()#       H = H + 1;
            self.generator.incVar(v1)#	tpuntero = tpuntero +1;
            self.generator.addGoto(loop)#   goto Loop
            self.generator.addLabel(lsalida)# Lsalida:
            self.generator.addSetHeap(index=tmpR,value=t_cont)# Heap[tmpR] = tcont //tamaño
            result.tipo = Tipos.INT64
            result.tipo_aux = Tipos.ARREGLO
            result.valor = tmpR
            result.isTemp = True
        else:
            error = "Una o ambas expresiones no son int o usize"
            print(error)
        return result