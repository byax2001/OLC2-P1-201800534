from models.Abstract.Instruction import Instruccion
from models.TablaSymbols.Enviroment import Enviroment
from models.Abstract import Expresion
from models import Driver
from models.TablaSymbols.ValC3d import ValC3d

class Return(Instruccion):
    def __init__(self, exp: Expresion, line:int, column:int):
        self.exp=exp
        self.line = line
        self.column = column
    def ejecutar(self, driver: Driver, ts: Enviroment):
        if self.exp==None:
            return None
        else:
            return self.exp
    def generarC3d(self,ts,ptr:int):
        self.generator.addComment("Return")
        posCorret = self.SentTranferenciaC(ts, ["Funcion"])
        if posCorret==True:
            tmp_index=self.generator.newTemp()

            if self.exp!=None:
                self.exp.generator=self.generator
                exp:ValC3d=self.exp.generarC3d(ts,ptr)
                self.generator.addExpression(target=tmp_index, left="P", right="0", operator="+")
                self.generator.addSetStack(index=tmp_index, value=exp.valor)
            self.generator.addCode("return_i")
        else:
            error = "Return no esta en una funcion"
            print(error)
