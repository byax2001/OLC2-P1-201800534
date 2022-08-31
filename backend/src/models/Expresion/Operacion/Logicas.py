from models.Expresion.Operacion.OperacionLog import OperacionLog, OperadorLog, getOperador
from models.TablaSymbols.Tipos import Tipos,definirTipo

class Logicas(OperacionLog): #de esta forma se esta indicando que aritmeticas hereda de Operacion
    #var Operacion: exp1: Expresion, operador, exp2: Expresion, linea, columna, expU
    def getTipo(self, driver, ts):
        value = self.getValor(driver, ts)
        return definirTipo(value)

    # get valor con condicionales
    def getValor(self, driver, ts):
        t_nodoIzq = self.exp1.getTipo(driver, ts)
        t_nodoDer = self.exp2.getTipo(driver, ts) if not self.expU else None
        if t_nodoIzq==t_nodoDer:
            if t_nodoIzq==Tipos.BOOLEAN:
                if self.operador==OperadorLog.AND:
                    return self.exp1.getValor(driver,ts) and self.exp2.getValor(driver,ts)
                elif self.operador==OperadorLog.OR:
                    return self.exp1.getValor(driver,ts) or self.exp2.getValor(driver,ts)
            else:
                print("Ambos datos a comparar deben de ser valores booleanos")
        elif t_nodoIzq==Tipos.BOOLEAN and t_nodoDer==None:
            if self.operador == OperadorLog.NOT:
                return not (self.exp1.getValor(driver, ts))
        else:
            print("Se intenta hacer una operacion Logica con uno o dos nodos no Booleanos")
    def ejecutar(self, driver, ts):
        """En la mayoria de expresiones no realiza nada"""
        pass