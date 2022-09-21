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
        self.generator.addComment("Metodo ToString o ToOwned")
        exp=self.exp.generarC3d(ts,ptr)
        newTemp=self.generator.newTemp()
        if exp.tipo == Tipos.STR or exp.tipo == Tipos.CHAR:
            self.generator.addExpression(target=newTemp,left=exp.valor,right="",operator="")
            return ValC3d(valor=newTemp,isTemp=True,tipo=Tipos.STRING)
        else:
            cadena=str(exp.valor)
            newTemp = self.generator.newTemp()  # = tnum
            self.generator.addExpression(newTemp, "H", "", "")  # en este caso : tnum = H;
            for char in cadena:
                self.generator.addSetHeap("H", str(ord(char)))  # heap[(int)num]=   ascii code
                self.generator.addNextHeap()  # H = H + 1
            self.generator.addSetHeap("H", "-1")  # heap[(int)num]= -1
            self.generator.addNextHeap()  # H = H + 1
            return ValC3d(valor=newTemp, isTemp=True, tipo=Tipos.STRING)

