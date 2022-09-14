from models.Abstract.Instruction import Instruccion
from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Symbol import Symbols
from models.Driver import Driver
from models.TablaSymbols.Enviroment import Enviroment
from BaseDatos.B_datos import B_datos
class Insert(Instruccion):
    def __init__(self,id:str,index:Expresion,exp:Expresion,line:int,column:int):
        self.id=id
        self.index=index
        self.exp=exp
        self.line=line
        self.column=column
    def ejecutar(self, driver: Driver, ts: Enviroment):
        symbol=ts.buscar(self.id)
        v_index=self.index.getValor(driver,ts)
        t_index=self.index.getTipo(driver,ts)
        if symbol!=None:  #si existe el vector, si ya fue declarado
            if symbol.mut==True:
                if symbol.tsimbolo==Symbols.VECTOR: #si lo que se llamo fue un vector
                    v_exp=self.exp.getValor(driver,ts)
                    t_exp=self.exp.getTipo(driver,ts)
                    if t_index==Tipos.INT64: #el index es un entero
                        if v_exp!=None and t_exp!=Tipos.ERROR:  #que el valor de la expresion a ingresar no de errores
                            if t_exp==symbol.tipo:  #que lo que se va a ingresar sea del mismo tipo que el vector
                                vector=symbol.value
                                vector.insert(v_index,{"valor":v_exp,"tipo":t_exp})
                            else:
                                print(f"Error Intento de Insert de un valor con un tipo distinto al vector linea:{self.line} ")
                                error = "Error Intento de Insert de un valor con un tipo distinto al vector"
                                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                                  columna=self.column)
                        else:
                            print(f"Expresion causa error al intentar hacer Insert  linea:{self.line} ")
                            error = "Expresion causa error al intentar hacer Insert"
                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                              columna=self.column)
                    else:
                        print(f"El index debe de ser un entero linea: {self.line}")
                        error = "El index debe de ser un entero linea"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                          columna=self.column)

                else:
                    print(f"Error Intento de Insert en una variable no vectorial  linea:{self.line} ")
                    error = "Error Intento de Insert en una variable no vectorial "
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
            else:
                print(f"Intento de Insert en vector no muteable linea: {self.line}")
                error = "Intento de Insert en vector no muteable "
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        else:
            print(f"Error Intento de Insert en vector no declarado linea:{self.line} ")
            error = "Error Intento de Insert en vector no declarado "
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)