#0..4 arreglo del 0 al  4 [1,2,3,4]
#"hola".char() arreglo ['h','o','l','a']
# array o vector
from models.Instruction.Instruction import Instruccion
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.Symbol import Symbol
from models.Driver import Driver
from models.TablaSymbols.Tipos import Tipos
class ForIn(Instruccion):
    def __init__(self,id:str,arreglo,cInst:[Instruccion],line:int,column:int):
        self.id=id
        self.arreglo=arreglo
        self.cInst=cInst
        self.line=line
        self.column=column
    def ejecutar(self, driver: Driver, ts: Enviroment):
        new_ts=Enviroment(ts,"ForIn")
        new_ts2=Enviroment(new_ts,"Bloque ForIn")
        cArr=self.arreglo.getValor(driver,ts)
        tArr=self.arreglo.getTipo(driver,ts)
        if type(cArr)==list:
            symbol=Symbol(mut=True,id=self.id,value="",tipo_simbolo=0,tipo=tArr,line=self.line,column=self.column)
            new_ts.addVar(self.id,symbol)
            for element in cArr:
                new_ts.updateForIn(self.id,element["valor"]) #actualizar variable id en cada iteracion
                for inst in self.cInst:
                    inst.ejecutar(driver,new_ts2)
        else:
            print("Error intento de for in en un elemento que no es arreglo o rango")

