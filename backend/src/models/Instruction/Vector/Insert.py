from models.Instruction.Instruction import Instruccion
from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Symbol import Symbols
from models.Driver import Driver
from models.TablaSymbols.Enviroment import Enviroment
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
                                print(vector.vector)
                                vector.insert(v_index,{"valor":v_exp,"tipo":t_exp})
                            else:
                                print(f"Error Intento de Insert de un valor con un tipo distinto al vector linea:{self.line} ")
                        else:
                            print(f"Expresion causa error al intentar hacer Insert  linea:{self.line} ")
                    else:
                        print(f"El index debe de ser un entero linea: {self.line}")
                else:
                    print(f"Error Intento de Insert en una variable no vectorial  linea:{self.line} ")
            else:
                print(f"Intento de Insert en vector no muteable linea: {self.line}")
        else:
            print(f"Error Intento de Insert en vector no declarado linea:{self.line} ")

        symbol2=ts.buscar(self.id)
        print(symbol2.value.vector)