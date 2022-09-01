from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
class CharArray(Expresion):
    def __init__(self,exp:Expresion,line:int,column:int):
        self.value=None
        self.tipo=None
        self.exp=exp
        self.line=line
        self.column=column
    def getValor(self, driver, ts):
        t_exp=self.exp.getTipo(driver,ts)
        if t_exp==Tipos.STR:
            v_exp=self.exp.getValor(driver,ts)
            vector=[]
            for i in v_exp:
                vector.append({"valor":i,"tipo":Tipos.CHAR})
            self.value=vector
            self.tipo=Tipos.CHAR
        else:
            print("Error chars() en un elemento no &str")
        return self.value
    #2x2
    #get tipo 4
    # get valor 8
    def getTipo(self, driver, ts):
        self.getValor(driver, ts)
        if self.value == None:
            self.tipo == Tipos.ERROR
        return self.tipo
    def ejecutar(self,driver,ts):
        pass
