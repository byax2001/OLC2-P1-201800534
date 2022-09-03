from models.Expresion.Operacion.OperacionRel import OperacionRel, OperadorRel, getOperador
from models.TablaSymbols.Tipos import Tipos,definirTipo

class Relacionales(OperacionRel): #de esta forma se esta indicando que aritmeticas hereda de Operacion
    #var Operacion: exp1: Expresion, operador, exp2: Expresion, linea, columna, expU
    def getTipo(self, driver, ts):
        self.resetInst()
        if self.tipo==None and self.value==None:
            self.getValor(driver, ts)
            if self.value==None:
                self.tipo==Tipos.ERROR
        else:
            self.instancia+=1
        return self.tipo

    # get valor con condicionales
    def getValor(self, driver, ts):
        self.instancia+=1
        if self.tipo==None and self.value==None:
            t_nodoIzq = self.exp1.getTipo(driver, ts)
            v_nodoIzq = self.exp1.getValor(driver, ts)
            t_nodoDer = self.exp2.getTipo(driver, ts)
            v_nodoDer = self.exp2.getValor(driver,ts)
            if t_nodoDer==t_nodoIzq:
                self.value= self.comparar(v_nodoIzq,v_nodoDer)
                self.tipo=definirTipo(self.value)
            elif t_nodoIzq in [Tipos.INT64, Tipos.USIZE] and t_nodoDer in [Tipos.INT64, Tipos.USIZE]:
                self.value=  self.comparar(v_nodoIzq,v_nodoDer)
                self.tipo = definirTipo(self.value)
            else:
                print("Las literales a comparar no son del mismo tipo ")
        return self.value
    def comparar(self,valor1,valor2):
        if self.operador == OperadorRel.MAYORQUE:
            return valor1 > valor2
        elif self.operador == OperadorRel.MENORQUE:
            return valor1 < valor2
        elif self.operador == OperadorRel.MAYORIGUALQUE:
            return valor1 >= valor2
        elif self.operador == OperadorRel.MENORIGUALQUE:
            return valor1 <= valor2
        elif self.operador == OperadorRel.IGUALQUE:
            return valor1 == valor2
        elif self.operador == OperadorRel.DIFERENTEQUE:
            return valor1 != valor2

    def ejecutar(self, driver, ts):
        """En la mayoria de expresiones no realiza nada"""
        pass
    def resetInst(self):
        if self.instancia>1:
            self.instancia=0
            self.value=None
            self.tipo=None