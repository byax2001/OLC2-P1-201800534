from models.Instruction.Instruction import Instruccion
from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models import Driver
from models.Instruction.Brazo import Brazo
from models.TablaSymbols.Tipos import Tipos,definirTipo

class While(Instruccion):
    def __init__(self,exp:Expresion,bloque:[Instruccion],line:int,column:int):
        self.exp=exp
        self.bloque=bloque
        self.line=line
        self.column=column
    def ejecutar(self, driver: Driver, ts: Enviroment):
        v_exp=self.exp.getValor(driver,ts)
        t_exp=self.exp.getTipo(driver,ts)
        if t_exp!=Tipos.ERROR and t_exp==Tipos.BOOLEAN:
            while(v_exp):
                Newts = Enviroment(ts, 'While')
                for element in self.bloque:
                    element.ejecutar(driver,Newts);
                v_exp=self.exp.getValor(driver,ts)
                t_exp = self.exp.getTipo(driver, ts)
                if t_exp == Tipos.ERROR and t_exp != Tipos.BOOLEAN:
                    print("La expresion da error o no es booleana")
                    return
        else:
            print("La expresion da error o no es booleana")
            return
