from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d

class Abs(Expresion):
    def __init__(self,exp:Expresion,line:int,column:int):
        super().__init__()
        self.exp=exp
        self.line=line
        self.column=column
    def getValor(self, driver, ts):
        #ABS NO FUNCIONA SI LA EXPRESION QUE SE INTENTA ANALIZAR NO ES UN ID
        if self.exp.getTipo(driver,ts) in [Tipos.FLOAT64,Tipos.INT64]:
            return abs(self.exp.getValor(driver,ts))
        else:
            error = "Error se esta intentando hacer abs a un dato no numerico"
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
            noNeg = self.generator.newLabel()
            self.generator.addExpAsign(target=tmpR,right=exp.valor)
            self.generator.addIf(left=tmpR,rigth="0",operator=">",label=noNeg)
            self.generator.addExpression(target=tmpR,left=tmpR,right="-1",operator="*")
            self.generator.addLabel(noNeg)
            result.tipo = exp.tipo
            result.valor = tmpR
            result.isTemp = True
        else:
            error="La expresion a hacer abs no es un numero"
            print(error)
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
        return result