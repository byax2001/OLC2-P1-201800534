from models.Instruction.Instruction import Instruccion
from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models import Driver
from models.Instruction.Break import Break
from models.Instruction.Return import Return
from models.Instruction.Continue import Continue
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
                    #si viene alguna de estas instrucciones cambiar el flujo
                    if isinstance(element, Break):
                        return
                    elif isinstance(element, Continue):
                        break;
                    elif isinstance(element, Return):
                        print("Error, existe return afuera de una funcion")
                        return
                    rInst=element.ejecutar(driver,Newts);

                    #si el resultado de ejecutar la instruccion devuelve alguno de estos cambiar el flujo
                    if isinstance(rInst, Break):
                        return
                    elif isinstance(rInst, Continue):
                        break;
                    elif isinstance(rInst, Return):
                        print("Error, existe return afuera de una funcion")
                        return

                v_exp=self.exp.getValor(driver,ts)
                t_exp = self.exp.getTipo(driver, ts)
                if t_exp == Tipos.ERROR and t_exp != Tipos.BOOLEAN:
                    print("La expresion da error o no es booleana")
                    return
        else:
            print("La expresion da error o no es booleana")
            return
