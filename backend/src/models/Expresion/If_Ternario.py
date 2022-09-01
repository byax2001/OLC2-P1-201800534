from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import definirTipo,Tipos


class If_ternario(Expresion):
    def __init__(self,exp:Expresion,expB1:Expresion,expB2:Expresion,line:int,column:int):
        self.value=None
        self.tipo=None
        self.exp=exp
        self.expB1=expB1
        self.expB2=expB2
        self.line=line
        self.column=column
        self.instancia=0
    def getTipo(self, driver, ts):
        if self.tipo is None or self.value is None:
            self.value = self.getValor(driver, ts)
            self.tipo = definirTipo(self.value)
            return self.tipo
        else:
            return self.tipo

    def getValor(self, driver, ts):
        self.instancia+=1
        self.resetInst()
        v_exp=self.exp.getValor(driver,ts);
        t_exp=self.exp.getTipo(driver,ts)
        if(v_exp is not None):
            if t_exp ==Tipos.BOOLEAN:
                if v_exp==True:
                    v_expB1= self.expB1.getValor(driver,ts)
                    return v_expB1
                else:
                    v_expB2 = self.expB2.getValor(driver, ts)
                    return v_expB2
            else:
                print("la expresion debe de dar un resultado booleano")
                return None
        else:
            print("La expresion en el if causa error")
            return None
    def resetInst(self):
        if self.instancia>2:
            self.instancia=0
            self.value=None
            self.tipo=None
    def ejecutar(self, driver, ts):
        """En la mayoria de expresiones no realiza nada"""
        pass