from models.Instruction.Instruction import Instruccion
from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Symbol import Symbols
from models.Driver import Driver
from models.TablaSymbols.Enviroment import Enviroment
class Push(Instruccion):
    def __init__(self,id:str,exp:Expresion,line:int,column:int):
        self.id=id
        self.exp=exp
        self.line=line
        self.column=column
    def ejecutar(self, driver: Driver, ts: Enviroment):
        symbol=ts.buscar(self.id)
        if symbol!=None:
            if symbol.mut==True:
                if symbol.tsimbolo==Symbols.VECTOR:
                    v_exp=self.exp.getValor(driver,ts)
                    t_exp=self.exp.getTipo(driver,ts)
                    if v_exp!=None and t_exp!=Tipos.ERROR:
                        if t_exp==symbol.tipo:
                            vector=symbol.value
                            vector.push({"valor":v_exp,"tipo":t_exp})

                        else:
                            print(f"Error Intento de push de un valor con un tipo distinto al vector linea:{self.line} ")
                    else:
                        print(f"Expresion causa error al intentar hacer push  linea:{self.line} ")
                else:
                    print(f"Error Intento de push en una variable no vectorial  linea:{self.line} ")
            else:
                print(f"Intento de Push en vector no muteable linea: {self.line}")
        else:
            print(f"Error Intento de push en vector no declarado linea:{self.line} ")
