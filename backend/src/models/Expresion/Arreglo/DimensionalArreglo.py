from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos,getTipo

class DimensionalArreglo(Expresion):
    def __init__(self,tipo:str,dimArr:Expresion,Dimensional:Expresion,line:int,column:int):
        self.valor=None
        self.tipo=getTipo(tipo) if tipo!="" else None
        self.Dim=Dimensional
        self.dimArr=dimArr
        self.column=column
        self.line=line

    #  tipo - dimensional  (no list)
    # [tipo; numero de valores]
    #     tipo                Dimensional  (list)
    # [[[tipo;numero de valores] ; numero de valores] ; numero de valores]

    def getValor(self, driver, ts):
        if self.valor==None:
            v_dim = self.Dim.getValor(driver, ts)
            t_dim = self.Dim.getTipo(driver,ts)

            if t_dim==Tipos.INT64:
                if self.dimArr==None:
                    self.valor=[v_dim]
                else:
                    arrayDim=self.dimArr.getValor(driver,ts)
                    arrayDim.insert(0, v_dim)
                    self.valor=arrayDim #Se agregan a la inversa para un mejor control pues por ejemplo
                                        # [[&str;2];4] es un array de 4 elementos con dos elementos adentro de cada uno de estos
                if self.tipo==None:
                    self.tipo=self.dimArr.getTipo(driver,ts)
            else:
                print(f"la dimensional debe de ser un entero linea: {self.line}")
        return self.valor


    def getTipo(self, driver, ts):
        if self.tipo==None:
            self.getValor(driver,ts)
            if self.valor==None: #si despues de eso aun es None entonces causa error la dimensional
                self.tipo=Tipos.ERROR
        return self.tipo

    def ejecutar(self,driver,ts):
        pass