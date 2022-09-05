from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.Driver import Driver
from models.TablaSymbols.Symbol import Symbols
from models.TablaSymbols.Tipos import Tipos,definirTipo
from BaseDatos.B_datos import B_datos

class Contains(Expresion):
    def __init__(self, id: str, exp: Expresion, line: int, column: int):
        self.value=None
        self.tipo=None
        self.id = id
        self.index = exp
        self.line = line
        self.column = column


    def ejecutar(self, driver: Driver, ts: Enviroment):
        self.getValor(driver,ts);
    def getValor(self, driver, ts):
        symbol = ts.buscar(self.id)
        t_exp = self.index.getTipo(driver, ts)
        v_exp = self.index.getValor(driver, ts)
        if symbol != None:  # si existe el vector, si ya fue declarado
            if symbol.tsimbolo == Symbols.VECTOR or symbol.tsimbolo==Symbols.ARREGLO:  # si lo que se llamo fue un vector o arreglo
                if t_exp != Tipos.ERROR and v_exp != None:
                    vector = symbol.value
                    self.value = vector.contains(v_exp)
                else:
                    print(f"La expresion a analizar da error: {self.line}")
                    error = "La expresion a analizar da error "
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
            else:
                print(f"Error Intento de Contain en una variable no vectorial o Arreglo  linea:{self.line} ")
                error = "Error Intento de Contain en una variable no vectorial o Arreglo "
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        else:
            print(f"Error Contain en vector o Arreglo no declarado linea:{self.line} ")
            error = "Error Contain en vector o Arreglo no declarado linea "
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
        return self.value

    def getTipo(self, driver, ts):
        self.tipo=definirTipo(self.getValor(driver,ts))
        return self.tipo