from models.Expresion.Operacion.OperacionLog import OperacionLog, OperadorLog, getOperador
from models.TablaSymbols.Tipos import Tipos,definirTipo

class Logicas(OperacionLog): #de esta forma se esta indicando que aritmeticas hereda de Operacion
    #var Operacion: exp1: Expresion, operador, exp2: Expresion, linea, columna, expU
    def getTipo(self, driver, ts):
        self.resetInst()
        if self.value==None and self.tipo==None:
            self.getValor(driver,ts)
            if self.value==None:
                self.tipo=Tipos.ERROR
        else:
            self.instancia+=1
        return self.tipo

    # get valor con condicionales
    def getValor(self, driver, ts):
        self.instancia+=1;

        if self.value==None and self.tipo==None:
            t_nodoIzq = self.exp1.getTipo(driver, ts)
            t_nodoDer = self.exp2.getTipo(driver, ts) if not self.expU else None
            if t_nodoIzq==t_nodoDer:
                if t_nodoIzq==Tipos.BOOLEAN:
                    if self.operador==OperadorLog.AND:
                        valor1 = self.exp1.getValor(driver, ts)
                        if valor1 == False:
                            self.value = False
                            valor2 = self.exp2.getValor(driver, ts)
                        else:
                            valor2 = self.exp2.getValor(driver, ts)
                            self.value = valor1 and valor2
                        self.tipo = Tipos.BOOLEAN
                    elif self.operador==OperadorLog.OR:
                        valor1=self.exp1.getValor(driver,ts)
                        if valor1==True:
                            self.value=True
                            valor2=self.exp2.getValor(driver,ts)
                        else:
                            valor2 = self.exp2.getValor(driver, ts)
                            self.value= valor1 or valor2
                        self.tipo = Tipos.BOOLEAN
                else:
                    print("Ambos datos a comparar deben de ser valores booleanos")
            elif t_nodoIzq==Tipos.BOOLEAN and t_nodoDer==None:
                if self.operador == OperadorLog.NOT:
                    self.value = not (self.exp1.getValor(driver, ts))
                    self.tipo = Tipos.BOOLEAN
            else:
                print("Se intenta hacer una operacion Logica con uno o dos nodos no Booleanos")
        return self.value
    def ejecutar(self, driver, ts):
        """En la mayoria de expresiones no realiza nada"""
        pass

    def resetInst(self):
        if self.instancia==2:
            self.instancia=0
            self.value=None
            self.tipo=None