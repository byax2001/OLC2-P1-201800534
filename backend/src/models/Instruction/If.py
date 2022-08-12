from models.Instruction.Instruction import Instruccion
from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.Tipos import Tipos

class If(Instruccion):
    def __init__(self,exp:Expresion,bloque1:[Instruccion],bloque2:[Instruccion],line:int,column:int):
        self.exp=exp
        self.bloque1=bloque1
        self.bloque2=bloque2
        self.line=line
        self.column=column

    def ejecutar(self, driver, ts: Enviroment):
        v_exp=self.exp.getValor(driver,ts);
        t_exp=self.exp.getTipo(driver,ts)
        if(v_exp is not None):
            if t_exp ==Tipos.BOOLEAN:
                if v_exp==True:
                    for element in self.bloque1:
                        element.ejecutar(driver,ts)
                else:
                    for element in self.bloque2:
                        element.ejecutar(driver, ts)
            else:
                print("la expresion debe de dar un resultado booleano")
        else:
            print("La expresion en el if causa error")