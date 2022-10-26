from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos,getTipo
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d

class DimensionalArreglo(Expresion):
    def __init__(self,tipo:str,dimArr:Expresion,Dimensional:Expresion,line:int,column:int):
        super().__init__()
        self.value=None
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
        if self.value == None:
            t_dim = self.Dim.getTipo(driver, ts)
            v_dim = self.Dim.getValor(driver, ts)

            if t_dim == Tipos.INT64 or t_dim==Tipos.USIZE:
                if self.dimArr == None:
                    self.value = [v_dim]
                else:
                    arrayDim = self.dimArr.getValor(driver, ts)
                    arrayDim.insert(0, v_dim)
                    self.value = arrayDim  # Se agregan a la inversa para un mejor control pues por ejemplo
                    # [[&str;2];4] es un array de 4 elementos con dos elementos adentro de cada uno de estos
                if self.tipo == None:
                    self.tipo = self.dimArr.getTipo(driver, ts)
            else:
                print(f"la dimensional debe de ser un entero linea: {self.line}")
                error = f"la dimensional debe de ser un entero "
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line, columna=self.column)
        return self.value

    def getTipo(self, driver, ts):
        if self.tipo == None:
            self.getValor(driver, ts)
            if self.value == None:  # si despues de eso aun es None entonces causa error la dimensional
                self.tipo = Tipos.ERROR
        return self.tipo

    def ejecutar(self, driver, ts):
        pass

    def generarC3d(self,ts,ptr):
        result=ValC3d(valor="0",isTemp=False,tipo=Tipos.ERROR,tipo_aux=Tipos.ERROR)
        if self.dimArr==None:
            self.Dim.generator=self.generator
            rDim:ValC3d=self.Dim.generarC3d(ts,ptr)
            if rDim.tipo in [Tipos.INT64,Tipos.USIZE]:
                tmpU=self.generator.newTemp()
                self.generator.addExpAsign(target=tmpU,right=rDim.valor)
                result.tipo=result.tipo_aux=self.tipo
                result.valor=[tmpU]
                result.isTemp=True
            else:
                error="Error: El tamaño de una parte del arreglo no es entero o usize"
                print(error)
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)

        else:
            self.dimArr.generator=self.generator
            self.Dim.generator=self.generator
            arrDim:ValC3d=self.dimArr.generarC3d(ts,ptr)
            rDim=self.Dim.generarC3d(ts,ptr)
            if rDim.tipo in [Tipos.INT64,Tipos.USIZE]:
                tmpU=self.generator.newTemp()
                self.generator.addExpAsign(target=tmpU,right=rDim.valor)
                result.tipo=arrDim.tipo
                result.tipo_aux = Tipos.ARREGLO
                arrDim.valor.insert(0, tmpU)  # Se agregan a la inversa para un mejor control pues por ejemplo
                result.valor=arrDim.valor
                # [[&str;2];4] es un array de 4 elementos con dos elementos adentro de cada uno de estos
                result.isTemp=True
            else:
                error="Error: El tamaño de una parte del arreglo no es entero o usize"
                print(error)
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        return result



