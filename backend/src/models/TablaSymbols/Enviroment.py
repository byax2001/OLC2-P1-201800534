from models.TablaSymbols.Symbol import Symbol,getSymbol

class Enviroment:
    def __init__(self,anterior,env) -> None:
        self.env=env
        self.anterior=anterior
        self.tabla={}
    
    def addVar(self, id: str, simbolo: Symbol):
        self.tabla[id] = simbolo

    def buscar(self, id: str) -> Symbol:
        ts = self
        while ts is not None:
            exist = ts.tabla.get(id)

            if exist is not None:
                return exist
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