from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import getTipo,Tipos,definirTipo
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d

class As(Expresion):
    def __init__(self, exp:Expresion,tipocast:str, line: int, column: int):
        super().__init__()
        self.value=None
        self.exp = exp
        self.tipo=getTipo(tipocast)
        self.line = line
        self.column = column
    def getValor(self, driver, ts):
        if self.exp.getTipo(driver,ts) in [Tipos.FLOAT64, Tipos.INT64]:
            valor=self.exp.getValor(driver,ts);
            if self.tipo==Tipos.INT64:
                return int(valor)
            elif self.tipo==Tipos.FLOAT64:
                return float(valor)
            elif self.tipo==Tipos.USIZE:
                return abs(int(valor))
            else:
                print("Casteo \"as\" no valido ")
                error = "Casteo \"as\" no valido "
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
                return None
        else:
            print("Error, intento de casteo \"as\" para un valor no float o int ")
            error = "Error, intento de casteo \"as\" para un valor no float o int "
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
    def getTipo(self, driver, ts):
        tipo=definirTipo(self.getValor(driver, ts))
        if self.tipo==Tipos.USIZE:
            tipo=Tipos.USIZE
        return tipo

    def generarC3d(self,ts,ptr):
        self.generator.addComment("--Caseteo As--")
        self.exp.generator = self.generator
        exp:ValC3d = self.exp.generarC3d(ts,ptr)
        result = ValC3d(valor="0",isTemp=False,tipo=Tipos.ERROR)
        if exp.tipo in [Tipos.FLOAT64, Tipos.INT64,Tipos.USIZE] and not exp.tipo_aux in [Tipos.ARREGLO,Tipos.VECTOR]:
            tmpR = self.generator.newTemp()
            if self.tipo==Tipos.INT64:
                self.generator.addExpAsign(target=tmpR,right=f"(int){exp.valor}")
            elif self.tipo==Tipos.FLOAT64:
                self.generator.addExpAsign(target=tmpR,right=f"(float){exp.valor}")
            elif self.tipo==Tipos.USIZE:
                self.generator.addExpAsign(target=tmpR,right=f"(int){exp.valor}")
                noNeg = self.generator.newLabel()
                self.generator.addIf(left=tmpR, rigth="0", operator=">", label=noNeg)
                self.generator.addExpression(target=tmpR, left=tmpR, right="-1", operator="*")
                self.generator.addLabel(noNeg)
            else:
                print("Casteo \"as\" no valido ")
                error = "Casteo \"as\" no valido "
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
            result.valor = tmpR
            result.tipo = self.tipo
            result.isTemp = True
            result.tipo_aux = self.tipo
        else:
            error = "Error, intento de casteo \"as\" para un valor no float, int o usize "
            print(error)
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
        return result
