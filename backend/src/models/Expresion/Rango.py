from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
class Rango(Expresion):
    def __init__(self, exp1:Expresion,exp2:Expresion,line:int,column:int):
        self.valor=None
        self.tipo=None
        self.exp1=exp1
        self.exp2=exp2
        self.line=line
        self.column=column
    def getValor(self, driver, ts):
        if self.valor==None and self.tipo==None:
            t_exp1 = self.exp1.getTipo(driver, ts)
            t_exp2 = self.exp2.getTipo(driver,ts)
            if t_exp1==Tipos.INT64 and t_exp2==Tipos.INT64:
                v_exp1=self.exp1.getValor(driver,ts)
                v_exp2=self.exp2.getValor(driver,ts)
                vector=[]
                for i in range(v_exp1,v_exp2):
                    vector.append({"valor":i,"tipo":Tipos.INT64})
                self.valor=vector
                self.tipo=Tipos.INT64
            else:
                print("Uno o los dos parametros de rango no son enteros o causan conflictos")
        return self.valor
    def getTipo(self, driver, ts):
        if self.tipo==None:
            self.getValor(driver,ts)
            if self.valor==None:
                self.tipo==Tipos.ERROR
        return self.tipo
    def ejecutar(self,driver,ts):
        pass