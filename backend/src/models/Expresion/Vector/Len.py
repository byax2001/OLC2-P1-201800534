from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import definirTipo
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d
from models.TablaSymbols.Symbol import Symbol,Symbols
from models.TablaSymbols.Tipos import Tipos

class Len(Expresion):
    def __init__(self,id:str,exp:Expresion,line:int,column:int,cIndex=[]):
        super().__init__()
        self.id=id
        self.value=None
        self.tipo=None
        self.exp = exp
        self.cIndexs=cIndex
        self.line=line
        self.column=column

    def ejecutar(self,driver,ts):
        pass
    def getValor(self, driver, ts):
        t_valor = self.exp.getTipo(driver, ts)
        valor=self.exp.getValor(driver,ts)
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

    def generarC3d(self,ts,ptr):
        self.generator.addComment(f"Len de Vector {self.id}")
        tmpR=self.generator.newTemp()
        result=ValC3d(valor=tmpR,isTemp=True,tipo=Tipos.ERROR)
        auxStack = self.generator.newTemp()
        symbol: Symbol = ts.buscarC3d(self.id, auxStack,self.en_funcion)
        if symbol != None:
            if symbol.tsimbolo == Symbols.VECTOR or symbol.tsimbolo == Symbols.ARREGLO:
                result.tipo = Tipos.INT64
                result.tipo_aux = Tipos.INT64
                t_puntero = self.generator.newTemp()
                self.generator.addBackStack(auxStack)
                auxIndex = self.generator.newTemp()
                self.generator.addExpression(target=auxIndex, left="P", right=str(symbol.position),
                                             operator="+")
                self.generator.addGetStack(target=t_puntero, index=auxIndex)
                self.generator.addNextStack(auxStack)
                self.generator.addGetHeap(target=tmpR, index=t_puntero)  # t_tam=inicioArray
            elif symbol.tipo == Tipos.STRING:
                print() #por si acaso es necesario saber el tamaño de un string
            else:
                error = "Se intenta usar len en un elemento no vector o arreglo"
                print(error)
        else:
            error = "No existe dicho arreglo"
            print(error)
        self.generator.addComment("End Insert")
        return result