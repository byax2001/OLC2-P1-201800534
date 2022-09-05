from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.Driver import Driver
from models.TablaSymbols.Symbol import Symbols
from models.TablaSymbols.Tipos import Tipos
from BaseDatos.B_datos import B_datos

class Remove(Expresion):
    def __init__(self, id: str, index: Expresion, line: int, column: int):
        self.value=None
        self.tipo=None
        self.id = id
        self.index = index
        self.line = line
        self.column = column
        self.instancia=0


    def ejecutar(self, driver: Driver, ts: Enviroment):
        self.getTipo(driver,ts)
        self.getValor(driver,ts);
    def getValor(self, driver, ts):
        self.instancia+=1
        if self.value==self.tipo==None:
            symbol = ts.buscar(self.id)
            t_index = self.index.getTipo(driver, ts)
            v_index = self.index.getValor(driver, ts)
            if symbol != None:  # si existe el vector, si ya fue declarado
                if symbol.mut == True:
                    if symbol.tsimbolo == Symbols.VECTOR:  # si lo que se llamo fue un vector
                        if t_index == Tipos.INT64 or t_index==Tipos.USIZE:  # el index es un entero
                            vector = symbol.value
                            self.value=vector.remove(v_index)

                            if self.value!=None:
                                self.tipo=symbol.tipo
                            else:
                                self.tipo=Tipos.ERROR
                        else:
                            print(f"El index debe de ser un entero linea: {self.line}")
                            error = "El index debe de ser un entero linea"
                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                              columna=self.column)
                    else:
                        print(f"Error Intento de Insert en una variable no vectorial  linea:{self.line} ")
                        error = "Error Intento de Insert en una variable no vectorial"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                          columna=self.column)
                else:
                    print(f"Intento de Insert en vector no muteable linea: {self.line}")
                    error = "Intento de Insert en vector no muteable"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
            else:
                print(f"Error Intento de Insert en vector no declarado linea:{self.line} ")
                error = "Error Intento de Insert en vector no declarado"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        return self.value

    def getTipo(self, driver, ts):
        self.resetInst()
        if self.value==self.tipo==None:
            self.getValor(driver,ts)
        else:
            self.instancia+=1
        return self.tipo
    def resetInst(self):
        if self.instancia>1:
            self.instancia=0
            self.value=None
            self.tipo=None