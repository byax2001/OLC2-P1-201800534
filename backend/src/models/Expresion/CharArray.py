from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
class CharArray(Expresion):
    def __init__(self,exp:Expresion,line:int,column:int):
        self.valor=None
        self.tipo=None
        self.exp=exp
        self.line=line
        self.column=column
        self.instancia=0
    def getValor(self, driver, ts):
        self.instancia+=1
        self.resetInst()
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
        return self.valor
    def getTipo(self, driver, ts):
        if self.tipo == None:
            self.getValor(driver, ts)
            if self.valor == None:
                self.tipo == Tipos.ERROR
        return self.tipo
    def ejecutar(self,driver,ts):
        pass

    def resetInst(self):
        if self.instancia>2:
            self.instancia=0
            self.value=None
            self.tipo=None