from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.Driver import Driver
from models.TablaSymbols.Symbol import Symbols,Symbol
from models.TablaSymbols.Tipos import definirTipo,Tipos
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d
class Capacity(Expresion):
    def __init__(self, id: str, line: int, column: int):
        super().__init__()
        self.value=None
        self.tipo=None
        self.id = id
        self.line = line
        self.column = column


    def ejecutar(self, driver: Driver, ts: Enviroment):
        pass
    def getValor(self, driver, ts):
        symbol = ts.buscar(self.id)
        if symbol != None:  # si existe el vector, si ya fue declarado
            if symbol.tsimbolo == Symbols.VECTOR:  # si lo que se llamo fue un vector
                vector = symbol.value
                self.value = vector.rcapacity()
            else:
                print(f"Error Intento de Contain en una variable no vectorial  linea:{self.line} ")
                error = "Error Intento de Contain en una variable no vectorial  "
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        else:
            print(f"Error Contain en vector no declarado linea:{self.line} ")
            error = "Error Contain en vector no declarado"
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
        return self.value

    def getTipo(self, driver, ts):
        self.tipo=definirTipo(self.getValor(driver,ts))
        return self.tipo

    def generarC3d(self,ts:Enviroment,ptr):
        tmp_aux=self.generator.newTemp()
        symbol:Symbol=ts.buscarC3d(self.id,tmp_aux)
        result=ValC3d(valor="0",isTemp=False,tipo=Tipos.ERROR)
        if symbol.tsimbolo==Symbols.VECTOR:
            tmpR=self.generator.newTemp()
            tindexA=self.generator.newTemp()
            tpuntero=self.generator.newTemp()
            self.generator.addBackStack(tmp_aux)
            self.generator.addExpression(target=tindexA,left="P",right=str(symbol.position),operator="+")
            self.generator.addNextStack(tmp_aux)
            self.generator.addGetStack(target=tpuntero,index=tindexA)
            self.generator.incVar(tpuntero)
            self.generator.addGetHeap(target=tmpR,index=tpuntero)
            result.valor=tmpR
            result.isTemp=True
            result.tipo=Tipos.INT64
            result.tipo_aux=Tipos.INT64
        else:
            error="Intento de capacity en una variable que no es vector"
            print(error)
        return result