from models.Expresion.Operacion.Operacion import Operacion, Operador, getOperacion
from models.TablaSymbols.Tipos import Tipos,definirTipo

class Aritmeticas(Operacion): #de esta forma se esta indicando que aritmeticas hereda de Operacion
    #var Operacion: exp1: Expresion, operador, exp2: Expresion, linea, columna, expU
    def getTipo(self, driver, ts):
        value = self.getValor(driver, ts)
        return definirTipo(value)

    # get valor con condicionales
    def getValor(self, driver, ts):
        t_nodoIzq = self.exp1.getTipo(driver, ts)
        t_nodoDer = self.exp2.getTipo(driver, ts) if not self.expU else None
        
        if self.expU is not None:
            if self.operador == Operador.UNARIO:
                return - self.exp1.getValor(driver, ts)
            else:
                # Error: la expresion unaria solo acepta el operador -
                pass

        if self.operador == Operador.SUMA:
            # INT + ?
            # FLOAT + ?
            if t_nodoIzq == t_nodoDer:
                if t_nodoIzq in [Tipos.INT64, Tipos.FLOAT64]:
                    return self.exp1.getValor(driver, ts) + self.exp2.getValor(driver, ts)
                elif t_nodoIzq in [Tipos.STRING]:
                    return self.exp1.getValor(driver, ts) +""+self.exp2.getValor(driver, ts)
            else:
                print(f'Los nodos no son del mismo valor', self.exp2.linea,
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
               print(f'Las expresiones a restar deben de ser del mismo tipo')
        elif self.operador == Operador.DIV:
            if t_nodoIzq == t_nodoDer:
                if t_nodoIzq in [Tipos.INT64, Tipos.FLOAT64]:
                    return self.exp1.getValor(driver, ts) / self.exp2.getValor(driver, ts)
                else:
                    print(f'Las expresiones para la  division debe ser un integer o float ', self.exp2.linea, self.exp2.columna)
            else:
               print(f'Las expresiones a restar deben de ser del mismo tipo')
        elif self.operador == Operador.MOD:
            if t_nodoIzq == t_nodoDer:
                if t_nodoIzq in [Tipos.INT64, Tipos.FLOAT64]:
                    return self.exp1.getValor(driver, ts) % self.exp2.getValor(driver, ts)
                else:
                    print(f'Las expresiones para la  division debe ser un integer o float ', self.exp2.linea, self.exp2.columna)
            else:
               print(f'Las expresiones a restar deben de ser del mismo tipo')
        elif self.operador == Operador.POW:
            if t_nodoIzq == t_nodoDer:
                if t_nodoIzq in [Tipos.INT64, Tipos.FLOAT64]:
                    return pow(self.exp1.getValor(driver, ts),self.exp2.getValor(driver, ts))
                else:
                    print(f'Las expresiones para la  division debe ser un integer o float ', self.exp2.linea, self.exp2.columna)
            else:
               print(f'Las expresiones a restar deben de ser del mismo tipo')
        else:
            print(f'La operacion {self.operador} no es soportado')

    def ejecutar(self, driver, ts):
        """En la mayoria de expresiones no realiza nada"""
        pass