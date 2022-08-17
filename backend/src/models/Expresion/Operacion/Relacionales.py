from models.Expresion.Operacion.OperacionRel import OperacionRel, OperadorRel, getOperador
from models.TablaSymbols.Tipos import Tipos,definirTipo

class Relacionales(OperacionRel): #de esta forma se esta indicando que aritmeticas hereda de Operacion
    #var Operacion: exp1: Expresion, operador, exp2: Expresion, linea, columna, expU
    def getTipo(self, driver, ts):
        value = self.getValor(driver, ts)
        return definirTipo(value)

    # get valor con condicionales
    def getValor(self, driver, ts):
        t_nodoIzq = self.exp1.getTipo(driver, ts)
        t_nodoDer = self.exp2.getTipo(driver, ts)
        if t_nodoDer==t_nodoIzq:
            if self.operador==OperadorRel.MAYORQUE:
                return self.exp1.getValor(driver,ts)>self.exp2.getValor(driver,ts)
            elif self.operador==OperadorRel.MENORQUE:
                return self.exp1.getValor(driver,ts)<self.exp2.getValor(driver,ts)
            elif self.operador==OperadorRel.MAYORIGUALQUE:
                return self.exp1.getValor(driver,ts)>=self.exp2.getValor(driver,ts)
            elif self.operador==OperadorRel.MENORIGUALQUE:
                return self.exp1.getValor(driver,ts)<=self.exp2.getValor(driver,ts)
            elif self.operador==OperadorRel.IGUALQUE:
                return self.exp1.getValor(driver,ts)==self.exp2.getValor(driver,ts)
            elif self.operador==OperadorRel.DIFERENTEQUE:
                return self.exp1.getValor(driver,ts)!=self.exp2.getValor(driver,ts)
        else:
            print("Las literales a comparar no son del mismo tipo ")
            return None
    def ejecutar(self, driver, ts):
        """En la mayoria de expresiones no realiza nada"""
        pass