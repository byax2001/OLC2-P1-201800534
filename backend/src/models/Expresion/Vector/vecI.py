from models.Instruction.Instruction import Instruccion
from models.TablaSymbols.Tipos import Tipos,definirTipo
from models.Expresion.Expresion import Expresion
#dec vector vacio
#  vectorI == vec!
class vecI(Expresion):
    def __init__(self,cExp:[Expresion],exp:Expresion,multiplicador:Expresion,line:int,column:int):
        self.value=None
        self.tipo=None
        self.cExp=cExp
        self.line=line
        self.column=column
        self.exp=exp
        self.multi=multiplicador
    def getValor(self, driver, ts):
        vector=[]
        if self.exp==None:
            x=0
            tipoaux=Tipos.ERROR
            for exp in self.cExp:
                if x==0:
                    tipoaux=exp.getTipo(driver,ts)
                    valor=exp.getValor(driver,ts)
                    vector.append({"valor":valor,"tipo":tipoaux})
                    x+=1
                else:
                    tipo2=exp.getTipo(driver,ts)
                    valor2=exp.getValor(driver,ts)
                    if tipo2!=tipoaux:
                        self.tipo==Tipos.ERROR
                        self.value=None
                        print("Error uno de los elementos del vector no es igual")
                        return
                    vector.append({"valor": valor2, "tipo": tipo2})
            self.value=vector
            self.tipo=tipoaux
        else:
            if self.multi.getTipo(driver,ts)==Tipos.INT64:
                valor=self.exp.getValor(driver,ts)
                tipo=self.exp.getTipo(driver,ts)
                if tipo!=Tipos.ERROR:
                    multi = self.multi.getValor(driver, ts)
                    self.tipo=tipo
                    x=0;
                    while x!=multi:
                        vector.append({"valor":valor,"tipo":tipo})
                        x+=1
                    self.value=vector
                    self.tipo=tipo
                else:
                    print("La expresion a multiplicar en una array da error"+str(self.line))
            else:
                print("Error el multiplicador no es integer")
        return self.value




    def getTipo(self, driver, ts):
        if self.value==None and self.tipo==None:
            self.getValor(driver,ts)
            if self.value == None:  # si despues de eso sigue siendo None ocurrio un error
                self.tipo = Tipos.ERROR
            return self.tipo
        else:
            return self.tipo
