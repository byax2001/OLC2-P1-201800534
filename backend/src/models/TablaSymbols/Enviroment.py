from models.TablaSymbols.Symbol import Symbol,getSymbol
from Generator3D.Generator3D import Generator
from models.TablaSymbols.SymC3d import SymC3d
class Enviroment:
    def __init__(self,anterior,env) -> None:
        self.generator=Generator()
        self.env=env
        self.anterior=anterior
        self.size=0
        self.tabla={}
    
    def addVar(self, id: str, simbolo: Symbol):
        self.tabla[id] = simbolo
        symc3d = SymC3d(id=id,type=simbolo.tipo,position=self.size,valor=simbolo.value)
        self.size = self.size + 1
        return symc3d

    def buscar(self, id: str) -> Symbol:
        ts = self
        while ts is not None:
            exist = ts.tabla.get(id)

            if exist is not None:
                return exist
            ts = ts.anterior

        return None

    def buscarC3d(self,id:str,tmp_aux):
        ts = self
        while ts is not None:
            exist = ts.tabla.get(id)
            if exist is not None:
                return exist
            ts = ts.anterior
            if ts!=None:
                self.generator.addExpression(target=tmp_aux,left=tmp_aux,right=str(ts.size),operator="+") #variable auxiliar que servira para volver a colocar el enviroment en su lugar  luego del proceso
        return None

    def actualizarC3d(self,id:str,value,isArray=False,prof_array=0):
        ts = self
        while ts is not None:
            symbol:Symbol = ts.tabla.get(id)

            if symbol is not None:
                symbol.value = value
                tmp_i = self.generator.newTemp()
                self.generator.addExpression(target=tmp_i, left="P", right=str(symbol.position), operator="+")
                self.generator.addSetStack(index=tmp_i,value=str(value))
                if isArray:
                    symbol.value.profundidad=prof_array  #value seria un objeto VectorC3d en ese caso
                                                         #asegurandose previamente que el simbolo es un vector o arreglo
                ts.tabla.update({id: symbol})

                return True
            ts = ts.anterior
        return None

    def actualizar(self,id:str,value):
        ts=self
        while ts is not None:
            symbol= ts.tabla.get(id)
            if symbol is not None:
                symbol.value=value
                ts.tabla.update({id:symbol})
                return True
            ts =ts.anterior
        return None

    def updateForIn(self,id:str,value):
        ts=self
        while ts is not None:
            symbol= ts.tabla.get(id)
            if symbol is not None:
                symbol.value=value
                if type(value) == list:
                    symbol.tsimbolo=getSymbol(1)
                elif type(value) != list:
                    symbol.tsimbolo=getSymbol(0)
                ts.tabla.update({id:symbol})
                return True
            ts =ts.anterior
        return None


    def buscarActualTs(self, id: str) -> Symbol:
        return self.tabla.get(id)