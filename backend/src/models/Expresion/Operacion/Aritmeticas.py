from models.Expresion.Operacion.Operacion import Operacion, Operador, getOperacion
from models.TablaSymbols.Tipos import Tipos,definirTipo
import math
class Aritmeticas(Operacion): #de esta forma se esta indicando que aritmeticas hereda de Operacion
    #var Operacion: exp1: Expresion, operador, exp2: Expresion, linea, columna, expU
    #ARITMETICAS TIENE UN CONSTRUCTOR HEREDADO POR "OPERACION"
    def getTipo(self, driver, ts):
        self.resetInst()
        if self.tipo==None and self.value==None:
            self.getValor(driver,ts)
            if self.value==None:
                self.tipo=Tipos.ERROR
        else:
            self.instancia+=1
        return self.tipo

    # get valor con condicionales
    def getValor(self, driver, ts):
        self.instancia+=1
        if self.value==None and self.tipo==None:
            t_nodoIzq = self.exp1.getTipo(driver, ts)
            t_nodoDer = self.exp2.getTipo(driver, ts) if not self.expU else None

            if self.expU ==True:
                self.value= - self.exp1.getValor(driver, ts)
                self.tipo=definirTipo(self.value)
                return self.value

            valorizq = self.exp1.getValor(driver, ts)
            valorder = self.exp2.getValor(driver, ts)
            if self.operador == Operador.SUMA:
                # INT + ?
                # FLOAT + ?
                if t_nodoIzq == t_nodoDer:
                    if t_nodoIzq in [Tipos.INT64, Tipos.FLOAT64]:
                        self.value= valorizq + valorder
                        self.tipo = definirTipo(self.value)
                elif t_nodoIzq in [Tipos.INT64, Tipos.USIZE] and t_nodoDer in [Tipos.INT64, Tipos.USIZE]:
                    self.value= valorizq + valorder
                    self.tipo = definirTipo(self.value)
                elif t_nodoIzq==Tipos.STRING and t_nodoDer==Tipos.STR:
                    self.value= str(valorizq) +str(valorder)
                    self.tipo = Tipos.STRING
                else:
                    print(f'Los nodos no son del mismo valor o no son posible de concatenar o sumar', self.exp2.linea,
                            self.exp2.columna)
            elif self.operador == Operador.RESTA:
                if t_nodoIzq == t_nodoDer:
                    if t_nodoIzq in [Tipos.INT64, Tipos.FLOAT64]:
                        self.value= valorizq - valorder
                        self.tipo = definirTipo(self.value)
                    else:
                        print(f'Las expresiones para la resta deben de ser un integer, float o usize ', self.exp2.linea, self.exp2.columna)
                elif t_nodoIzq in [Tipos.INT64, Tipos.USIZE] and t_nodoDer in [Tipos.INT64, Tipos.USIZE]:
                    self.value= valorizq - valorder
                    self.tipo = definirTipo(self.value)
                else:
                    print(f'Las expresiones a restar deben de ser del mismo  {self.exp1.linea}')

            elif self.operador == Operador.MULTI:
                if t_nodoIzq == t_nodoDer:
                    if t_nodoIzq in [Tipos.INT64, Tipos.FLOAT64]:
                        self.value= valorizq * valorder
                        self.tipo = definirTipo(self.value)
                    else:
                        print(f'Las expresiones para la  multiplicacion debe ser un integer o float ', self.exp2.linea, self.exp2.columna)
                elif t_nodoIzq in [Tipos.INT64, Tipos.USIZE] and t_nodoDer in [Tipos.INT64, Tipos.USIZE]:
                    self.value= valorizq * valorder
                    self.tipo = definirTipo(self.value)
                else:
                   print(f'Las expresiones a multiplicar deben de ser del mismo tipo')
            elif self.operador == Operador.DIV:
                if t_nodoIzq == t_nodoDer:
                    v_exp1 = valorizq
                    v_exp2 = valorder
                    if v_exp2!=0:
                        if t_nodoIzq==Tipos.INT64:
                            self.value= math.trunc(v_exp1/ v_exp2)
                            self.tipo = definirTipo(self.value)
                        elif t_nodoIzq ==Tipos.FLOAT64:
                            self.value= v_exp1 / v_exp2
                            self.tipo = definirTipo(self.value)
                        else:
                            print(f'Las expresiones para la  division debe ser un integer o float ', self.exp2.linea, self.exp2.columna)
                    else:
                        print("Error: Se intenta dividir entre 0")
                elif t_nodoIzq in [Tipos.INT64, Tipos.USIZE] and t_nodoDer in [Tipos.INT64, Tipos.USIZE]:
                    v_exp1 = valorizq
                    v_exp2 = valorder
                    if v_exp2!=0:
                        self.value= math.trunc(v_exp1/ v_exp2)
                        self.tipo = definirTipo(self.value)
                    else:
                        print("Error: Se intenta dividir entre 0")
                else:
                   print(f'Las expresiones a dividir deben de ser del mismo tipo')
            elif self.operador == Operador.MOD:
                if t_nodoIzq == t_nodoDer:
                    if t_nodoIzq==Tipos.INT64:
                        self.value= valorizq % valorder
                        self.tipo = definirTipo(self.value)
                    elif t_nodoIzq==Tipos.FLOAT64:
                        self.value= float(valorizq % valorder)
                        self.tipo = definirTipo(self.value)
                    else:
                        print(f'Las expresiones para usar el operador modulo debe ser un integer o float ', self.exp2.linea, self.exp2.columna)
                elif t_nodoIzq in [Tipos.INT64, Tipos.USIZE] and t_nodoDer in [Tipos.INT64, Tipos.USIZE]:
                    self.value= valorizq % valorder
                    self.tipo = definirTipo(self.value)
                else:
                   print(f'Las expresiones a hacer mod deben de ser del mismo tipo')
            elif self.operador == Operador.POW:
                if t_nodoIzq == t_nodoDer:
                    if t_nodoIzq ==Tipos.INT64:
                        self.value= pow(valorizq,valorder)
                        self.tipo = definirTipo(self.value)
                    else:
                        print(f'Las expresiones para el operador pow debe ser un integer ', self.exp2.linea, self.exp2.columna)
                elif t_nodoIzq in [Tipos.INT64, Tipos.USIZE] and t_nodoDer in [Tipos.INT64, Tipos.USIZE]:
                    self.value= pow( valorizq, valorder )
                    self.tipo = definirTipo(self.value)
                else:
                   print(f'Las expresiones a elevar deben de ser del mismo tipo')
            elif self.operador == Operador.POWF:
                if t_nodoIzq == t_nodoDer:
                    if t_nodoIzq==Tipos.FLOAT64:
                        self.value= pow(valorizq,valorder)
                        self.tipo = definirTipo(self.value)
                    else:
                        print(f'Las expresiones para el operador powf deben de ser float ', self.exp2.linea, self.exp2.columna)
                else:
                   print(f'Las expresiones a elevar deben de ser del mismo tipo')
            else:
                print(f'La operacion {self.operador} no es soportado')
        return self.value

    def resetInst(self):
        if self.instancia>1:
            self.instancia=0
            self.value=None
            self.tipo=None
    def ejecutar(self, driver, ts):
        """En la mayoria de expresiones no realiza nada"""
        pass