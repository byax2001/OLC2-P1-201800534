from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Enviroment import Enviroment
from models.Abstract.Expresion import Expresion
from BaseDatos.B_datos import B_datos
class If_ternario(Expresion):
    def __init__(self,exp:Expresion,bloque1:[],exp1b:Expresion,bloque2:[],exp2b:Expresion,line:int,column:int):
        self.value=None
        self.tipo=None
        self.exp=exp
        self.bloque1=bloque1
        self.bloque2=bloque2
        self.exp1b=exp1b
        self.exp2b=exp2b
        self.line=line
        self.column=column
        self.instancia=0
    def getTipo(self, driver, ts):
        self.resetInst()
        if self.tipo==None and self.value==None:
            self.getValor(driver,ts)
            if self.value==None:
                self.tipo==Tipos.ERROR
        else:
            self.instancia+=1

        return self.tipo

    def getValor(self, driver, ts):
        self.instancia+=1
        if self.tipo == None and self.value == None:
            newts=Enviroment(ts,"If ternario");
            t_exp = self.exp.getTipo(driver, ts)
            v_exp=self.exp.getValor(driver,ts);
            if(v_exp is not None):
                if t_exp == Tipos.BOOLEAN:
                    if v_exp==True:
                        for inst in self.bloque1:
                            inst.ejecutar(driver,newts)
                        expR=self.exp1b
                        self.tipo = expR.getTipo(driver, newts)
                        self.value=expR.getValor(driver,newts)
                    else:
                        for inst in self.bloque2:
                            inst.ejecutar(driver, newts)
                        expR = self.exp2b
                        self.tipo = expR.getTipo(driver, newts)
                        self.value = expR.getValor(driver, newts)
                else:
                    print("la expresion debe de dar un resultado booleano")
                    error = "la expresion debe de dar un resultado booleano"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
            else:
                print("La expresion en el if causa error")
                error = "La expresion en el if causa error"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        return self.value


    def resetInst(self):
        if self.instancia>1:
            self.instancia=0
            self.value=None
            self.tipo=None
    def ejecutar(self, driver, ts):
        """En la mayoria de expresiones no realiza nada aqui"""
        pass