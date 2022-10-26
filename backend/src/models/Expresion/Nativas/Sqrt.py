from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
import math
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d
class Sqrt(Expresion):
    def __init__(self,exp:Expresion,line:int,column:int):
        super().__init__()
        self.exp=exp
        self.line=line
        self.column=column
    def getValor(self, driver, ts):
        if self.exp.getTipo(driver,ts) == Tipos.FLOAT64:
            return math.sqrt(self.exp.getValor(driver,ts))
        elif self.exp.getTipo(driver,ts) == Tipos.INT64:
            return math.trunc(math.sqrt(self.exp.getValor(driver, ts)))
        else:
            error = "Error se esta intentando hacer sqrt a un dato no numerico"
            print(error)
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
    def getTipo(self, driver, ts):
        if self.exp.getTipo(driver, ts) in [Tipos.FLOAT64, Tipos.INT64]:
            return self.exp.getTipo(driver,ts)
        else:
            return Tipos.ERROR
    def ejecutar(self,driver,ts):
        pass

    def generarC3d(self,ts,ptr):
        result = ValC3d(valor="0",isTemp=False,tipo=Tipos.ERROR)
        self.exp.generator=self.generator
        exp : ValC3d = self.exp.generarC3d(ts,ptr)
        if exp.tipo in [Tipos.INT64,Tipos.FLOAT64,Tipos.USIZE]:
            tmpR = self.generator.newTemp()
            tnum = self.generator.newTemp()
            tsqrt = self.generator.newTemp()
            loop = self.generator.newLabel()
            t = self.generator.newTemp()
            taux = self.generator.newTemp()
            self.generator.addExpAsign(target=tnum,right=exp.valor)# tnum = val
            self.generator.addExpression(target=tsqrt,left=tnum,right="2",operator="/")# tsqrt = tnum /2;
            self.generator.addLabel(loop)# Loop:
            self.generator.addExpAsign(target=t,right=tsqrt)# t= tsqrt
            self.generator.addExpression(target=tsqrt,left=tnum,right=t,operator="/")# tsqrt = tnum /t
            self.generator.addExpression(target=tsqrt,left=tsqrt,right=t,operator="+")# tsqrt = tsqrt + t
            self.generator.addExpression(target=tsqrt,left=tsqrt,right="2",operator="/")# tsqrt = tsqrt /2
            self.generator.addExpression(target=taux,left=t,right=tsqrt,operator="-")# taux =t - tsqrt
            self.generator.addIf(left=taux,rigth="0",operator="!=",label=loop)# if (taux != 0) goto Loop
            self.generator.addExpAsign(target=tmpR,right=tsqrt)# tmpR = tsqrt
            result.tipo = exp.tipo
            result.valor = tmpR
            result.isTemp = True
        else:
            error="La expresion a hacer abs no es un numero"
            print(error)
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
        return result