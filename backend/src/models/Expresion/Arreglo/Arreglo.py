from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.Enviroment import Enviroment
class Arreglo(Expresion):
    def __init__(self,cExp:Expresion,exp:Expresion,multi:Expresion,line:int,column:int):
        self.value=None
        self.tipo=None
        self.cExp=cExp # ["hola","hola","hola"]
        self.exp=exp   #[ "hola" ; 3 ]
        self.multi=multi
        self.line=line
        self.column=column
        self.instancia=0
    def getValor(self, driver, ts:Enviroment):
        self.instancia += 1
        vector=[]
        if self.tipo==None and self.value==None:
            x = 0
            tipoaux = Tipos.ERROR
            if self.exp==None: #expresion a multiplicar

                for exp in self.cExp:
                    if x == 0:
                        tipoaux = exp.getTipo(driver, ts)
                        valor = exp.getValor(driver, ts)
                        vector.append({"valor": valor, "tipo": tipoaux})
                        x += 1
                    else:
                        tipo2 = exp.getTipo(driver, ts)
                        valor2 = exp.getValor(driver, ts)
                        if tipo2 != tipoaux:
                            self.tipo == Tipos.ERROR
                            self.value = None
                            print(f"Error uno de los elementos del arreglo no es del mismo tipo al resto linea: {self.line}")
                            error = f"Error uno de los elementos del arreglo no es del mismo tipo al resto"
                            B_datos().appendE(descripcion=error,ambito=ts.env,linea=self.line,columna=self.column)
                            return
                        vector.append({"valor": valor2, "tipo": tipo2})
                self.value = vector
                self.tipo = tipoaux
            else:
                v_exp=self.exp.getValor(driver,ts)
                t_exp=self.exp.getTipo(driver,ts)
                v_mult=self.multi.getValor(driver,ts)
                t_mult=self.multi.getTipo(driver,ts)
                if t_mult==Tipos.INT64 and t_exp!=Tipos.ERROR:
                    for x in range(v_mult):
                        vector.append({"valor":v_exp,"tipo":t_exp})
                    self.tipo=t_exp
                    self.value = vector
                else:
                    self.tipo=Tipos.ERROR
                    print(f"Error el numero de veces a multiplicar la expresion no es entero o la expresion causa error {self.line}")
                    error = f"Error el numero de veces a multiplicar la expresion no es entero o la expresion causa error"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line, columna=self.column)
        return self.value
    def getTipo(self, driver, ts):
        self.resetInst()
        if self.tipo==None and self.value==None:
            self.getValor(driver,ts)
            if self.tipo==None:
                self.tipo==Tipos.ERROR
        else:
            self.instancia+=1
        return self.tipo
    def ejecutar(self,driver,ts):
        pass
    def resetInst(self):
        if self.instancia>1:
            self.instancia=0
            self.value=None
            self.tipo=None