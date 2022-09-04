from models.Instruction.Instruction import Instruccion
from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.Tipos import Tipos
from models.Instruction.Break import Break
from models.Instruction.Continue import Continue
from models.Instruction.Return import Return

class If(Instruccion):
    def __init__(self,exp:Expresion,bloque1:[Instruccion],bloque2:[Instruccion],line:int,column:int):
        self.exp=exp
        self.bloque1=bloque1
        self.bloque2=bloque2
        self.line=line
        self.column=column

    def ejecutar(self, driver, ts: Enviroment):
        t_exp = self.exp.getTipo(driver, ts);
        v_exp=self.exp.getValor(driver,ts); # con el ts anterior
        new_ts=Enviroment(ts,"IF"); #ejecutar resto de instrucciones con el nuevo ts
        if(v_exp is not None):
            if t_exp ==Tipos.BOOLEAN:
                if v_exp==True:
                    for element in self.bloque1:
                        if isinstance(element,Break) or isinstance(element,Continue) or isinstance(element,Return):
                            return element
                        rInst=element.ejecutar(driver,new_ts)
                        if isinstance(rInst,Break) or isinstance(rInst,Continue) or isinstance(rInst,Return):
                            return rInst
                else:
                    for element in self.bloque2:
                        if isinstance(element, Break) or isinstance(element, Continue) or isinstance(element, Return):
                            return element
                        rInst = element.ejecutar(driver,new_ts)
                        if isinstance(rInst, Break) or isinstance(rInst, Continue) or isinstance(rInst, Return):
                            return rInst
            else:
                print("la expresion debe de dar un resultado booleano")
        else:
            print("La expresion en el if causa error")