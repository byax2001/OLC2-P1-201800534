from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d
class CharArray(Expresion):
    def __init__(self,exp:Expresion,line:int,column:int):
        super().__init__()
        self.valor=None
        self.tipo=None
        self.exp=exp
        self.line=line
        self.column=column
        self.instancia=0
    def getValor(self, driver, ts):
        self.instancia+=1
        if self.valor==None and self.tipo==None:
            t_exp=self.exp.getTipo(driver,ts)
            if t_exp==Tipos.STR:
                v_exp=self.exp.getValor(driver,ts)
                vector=[]
                for i in v_exp:
                    vector.append({"valor":i,"tipo":Tipos.CHAR})
                self.valor=vector
                self.tipo=Tipos.CHAR
            else:
                print("Error chars() en un elemento no &str")
                error = "Error chars() en un elemento no &str"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        return self.valor
    def getTipo(self, driver, ts):
        self.resetInst()
        if self.tipo == None:
            self.getValor(driver, ts)
            if self.valor == None:
                self.tipo == Tipos.ERROR
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
        self.generator.addComment("Char Array")
        result = ValC3d(valor="0",isTemp=False,tipo=Tipos.ERROR)
        self.exp.generator=self.generator
        rExp:ValC3d = self.exp.generarC3d(ts,ptr)
        if rExp.tipo == Tipos.STR or rExp.tipo == Tipos.STRING:
            t_puntero = self.generator.newTemp()
            t_cont = self.generator.newTemp()
            loop = self.generator.newLabel()
            lsalida = self.generator.newLabel()
            t1 = self.generator.newTemp()
            tmpR = self.generator.newTemp()
            self.generator.addExpAsign(t_puntero,right=rExp.valor)# tpuntero = tpunteroString
            self.generator.addExpAsign(target=t_cont,right="0")# tcont = 0
            self.generator.addExpAsign(target=tmpR, right="H")# tmpR = H
            self.generator.addNextHeap()# H = H + 1;
            self.generator.addLabel(loop)# Loop:
            self.generator.addGetHeap(target=t1,index=t_puntero)#   t1 = Heap[tpuntero]
            self.generator.addIf(left=t1,rigth="-1",operator="==",label=lsalida)#   if (t1 == -1 ) goto Lsalida
            self.generator.incVar(t_cont)#	tcont = tcont +1
            self.generator.addSetHeap(index="H",value=t1)#	Heap[H] = t1
            self.generator.addNextHeap()#       H = H + 1;
            self.generator.incVar(t_puntero)#	tpuntero = tpuntero +1;
            self.generator.addGoto(loop)#   goto Loop
            self.generator.addLabel(lsalida)# Lsalida:
            self.generator.addSetHeap(index=tmpR,value=t_cont)# Heap[tmpR] = tcont //tamaño
            result.tipo = Tipos.CHAR
            result.tipo_aux = Tipos.ARREGLO
            result.valor = tmpR
            result.isTemp = True
        else:
            error = "La expresion no es un string o &str"
            print(error)
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
        return result