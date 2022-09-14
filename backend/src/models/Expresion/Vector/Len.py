from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import definirTipo
from BaseDatos.B_datos import B_datos

class Len(Expresion):
    def __init__(self,exp:Expresion,line:int,column:int):
        self.value=None
        self.tipo=None
        self.exp = exp
        self.line=line
        self.column=column

    def ejecutar(self,driver,ts):
        pass
    def getValor(self, driver, ts):
        valor=self.exp.getValor(driver,ts)
        t_valor=self.exp.getTipo(driver,ts)
        if type(valor)==list or type(valor)==str:
            self.value=len(valor)
        else:
            print("Atributo no posee metodo len")
            error = "Atributo no posee metodo len"
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
        return self.value
    def getTipo(self, driver, ts):
        self.tipo=definirTipo(self.getValor(driver,ts))
        return self.tipo