from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
from BaseDatos.B_datos import B_datos
class Rango(Expresion):
    def __init__(self, exp1:Expresion,exp2:Expresion,line:int,column:int):
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