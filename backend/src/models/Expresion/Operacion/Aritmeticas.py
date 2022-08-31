from models.Expresion.Operacion.Operacion import Operacion, Operador, getOperacion
from models.TablaSymbols.Tipos import Tipos,definirTipo
import math
class Aritmeticas(Operacion): #de esta forma se esta indicando que aritmeticas hereda de Operacion
    #var Operacion: exp1: Expresion, operador, exp2: Expresion, linea, columna, expU
    #ARITMETICAS TIENE UN CONSTRUCTOR HEREDADO POR "OPERACION"
    def getTipo(self, driver, ts):
        if self.operador==Operador.SUMA and self.exp1.getTipo(driver,ts)==Tipos.STRING and self.exp2.getTipo(driver,ts)==Tipos.STR:
            self.tipo=Tipos.STRING
            return self.tipo
        else:
            self.value = self.getValor(driver, ts)
            self.tipo=definirTipo(self.value)
            return self.tipo

    # get valor con condicionales
    def getValor(self, driver, ts):
        t_nodoIzq = self.exp1.getTipo(driver, ts)
        t_nodoDer = self.exp2.getTipo(driver, ts) if not self.expU else None
        
        if self.expU ==True:
            return - self.exp1.getValor(driver, ts)

        if self.operador == Operador.SUMA:
            # INT + ?
            # FLOAT + ?
            if t_nodoIzq == t_nodoDer:
                if t_nodoIzq in [Tipos.INT64, Tipos.FLOAT64]:
                    return self.exp1.getValor(driver, ts) + self.exp2.getValor(driver, ts)
            elif t_nodoIzq==Tipos.STRING and t_nodoDer==Tipos.STR:
                return str(self.exp1.getValor(driver, ts)) +str(self.exp2.getValor(driver, ts))
            else:
                print(f'Los nodos no son del mismo valor o no son posible de concatenar o sumar', self.exp2.linea,
                        self.exp2.columna)
        elif self.operador == Operador.RESTA:
            if t_nodoIzq == t_nodoDer:
                if t_nodoIzq in [Tipos.INT64, Tipos.FLOAT64]:
                    return self.exp1.getValor(driver, ts) - self.exp2.getValor(driver, ts)
                else:
                    print(f'Las expresiones para la resta deben de ser un integer o float ', self.exp2.linea, self.exp2.columna)
            else:
               print(f'Las expresiones a restar deben de ser del mismo tipo')
        elif self.operador == Operador.MULTI:
            if t_nodoIzq == t_nodoDer:
                if t_nodoIzq in [Tipos.INT64, Tipos.FLOAT64]:
                    return self.exp1.getValor(driver, ts) * self.exp2.getValor(driver, ts)
                else:
                    print(f'Las expresiones para la  multiplicacion debe ser un integer o float ', self.exp2.linea, self.exp2.columna)
            else:
               print(f'Las expresiones a multiplicar deben de ser del mismo tipo')
        elif self.operador == Operador.DIV:
            if t_nodoIzq == t_nodoDer:
                v_exp1 = self.exp1.getValor(driver, ts)
                v_exp2 = self.exp2.getValor(driver, ts)
                if v_exp2!=0:
                    if t_nodoIzq==Tipos.INT64:
                        return math.trunc(v_exp1/ v_exp2)
                    elif t_nodoIzq ==Tipos.FLOAT64:
                        return v_exp1 / v_exp2
                    else:
                        print(f'Las expresiones para la  division debe ser un integer o float ', self.exp2.linea, self.exp2.columna)
                else:
                    print("Error: Se intenta dividir entre 0")
            else:
               print(f'Las expresiones a dividir deben de ser del mismo tipo')
        elif self.operador == Operador.MOD:
            if t_nodoIzq == t_nodoDer:
                if t_nodoIzq==Tipos.INT64:
                    return self.exp1.getValor(driver, ts) % self.exp2.getValor(driver, ts)
                elif t_nodoIzq==Tipos.FLOAT64:
                    return float(self.exp1.getValor(driver, ts) % self.exp2.getValor(driver, ts))
                else:
                    print(f'Las expresiones para usar el operador modulo debe ser un integer o float ', self.exp2.linea, self.exp2.columna)
            else:
               print(f'Las expresiones a hacer mod deben de ser del mismo tipo')
        elif self.operador == Operador.POW:
            if t_nodoIzq == t_nodoDer:
                if t_nodoIzq ==Tipos.INT64:
                    return pow(self.exp1.getValor(driver, ts),self.exp2.getValor(driver, ts))
                else:
                    print(f'Las expresiones para el operador pow debe ser un integer ', self.exp2.linea, self.exp2.columna)
            else:
               print(f'Las expresiones a elevar deben de ser del mismo tipo')
        elif self.operador == Operador.POWF:
            if t_nodoIzq == t_nodoDer:
                if t_nodoIzq==Tipos.FLOAT64:
                    return pow(self.exp1.getValor(driver, ts),self.exp2.getValor(driver, ts))
                else:
                    print(f'Las expresiones para el operador powf deben de ser float ', self.exp2.linea, self.exp2.columna)
            else:
               print(f'Las expresiones a elevar deben de ser del mismo tipo')
        else:
            print(f'La operacion {self.operador} no es soportado')

    def ejecutar(self, driver, ts):
        """En la mayoria de expresiones no realiza nada"""
        pass