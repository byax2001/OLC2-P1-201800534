from models.TablaSymbols.Symbol import Symbol

class Enviroment:
    def __init__(self,anterior,env) -> None:
        self.env=env
        self.anterior=anterior
        self.tabla={}
    
    def add(self, id: str, simbolo: Symbol):
        self.tabla[id] = simbolo

    def buscar(self, id: str) -> Symbol:
        ts = self
        while ts is not None:
            exist = ts.tabla.get(id)

            if exist is not None:
                return exist

            ts = ts.anterior

        return None

    def buscarActual(self, id: str) -> Symbol:
        return self.tabla.get(id)