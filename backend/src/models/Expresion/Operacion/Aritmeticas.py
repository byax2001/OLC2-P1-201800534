from models.Expresion.Operacion.Operacion import Operacion, Operador, getOperacion
from models.TablaSymbols.Types import Types, definirTipo

class Aritmeticas(Operacion): #de esta forma se esta indicando que aritmeticas hereda de Operacion
    #var Operacion: exp1: Expresion, operador, exp2: Expresion, linea, columna, expU
    def getTipo(self, driver, ts):
        value = self.getValor(driver, ts)
        return definirTipo(value)

    # get Valor con Diccionarios
    def getValor(self, driver, ts):
        if not self.expU:
            valor_exp1 = self.exp1.getValor(driver, ts)
            valor_exp2 = self.exp2.getValor(driver, ts)

            operacion = matriz_operaciones[self.operador]
            nodoIzq = operacion[self.exp1.getTipo(driver, ts)]
            funcion = nodoIzq[self.exp2.getTipo(driver, ts)]

            return funcion(valor_exp1, valor_exp2)

    # get valor con condicionales
    def getValor2(self, driver, ts):
        nodoIzq = self.exp1.getTipo(driver, ts)
        nodoDer = self.exp2.getTipo(driver, ts) if not self.expU else None

        if self.expU is not None:
            if self.operador == Operador.UNARIO:
                return - self.exp1.getValor(driver, ts)
            else:
                # Error: la expresion unaria solo acepta el operador -
                pass

        if self.operador == Operador.SUMA:
            # INT + ?
            # FLOAT + ?
            if nodoIzq in [Types.INT64, Types.FLOAT64]:
                # INT + INT
                # INT + FLOAT
                # FLOAT + INT
                # FLOAT + FLOAT
                if nodoDer in [Types.INT64, Types.FLOAT64]:
                    return self.exp1.getValor(driver, ts) + self.exp2.getValor(driver, ts)
                else:
                    print(f'La 2da expresion de la suma debe ser un integer o float ', self.exp2.linea,
                          self.exp2.columna)
            else:
                print(f'La 1er expresion de la suma debe ser un integer o float ', self.exp2.linea, self.exp2.columna)

        elif self.operador == Operador.RESTA:
            if nodoIzq == Types.INT64:
                if nodoDer == Types.INT64:
                    return self.exp1.getValor(driver, ts) - self.exp2.getValor(driver, ts)
                else:
                    print(f'La 2da expresion de la resta debe ser del mismo tipo')

            elif nodoIzq == Types.FLOAT64:
                if nodoDer == Types.FLOAT64:
                    return self.exp1.getValor(driver, ts) - self.exp2.getValor(driver, ts)
                else:
                    print(f'La 2da expresion de la resta debe ser del mismo tipo')
            else:
                print(f'La 1er expresion de la resta debe ser un integer o float ', self.exp2.linea, self.exp2.columna)

        elif self.operador == Operador.MULTI:
            if nodoIzq in [Types.INT64, Types.FLOAT64]:
                if nodoDer in [Types.INT64, Types.FLOAT64]:
                    return self.exp1.getValor(driver, ts) * self.exp2.getValor(driver, ts)
                else:
                    print(f'La 2da expresion de la multiplicacion debe ser un integer o float ', self.exp2.linea,
                          self.exp2.columna)
            else:
                print(f'La 1er expresion de la multiplicacion debe ser un integer o float ', self.exp2.linea,
                      self.exp2.columna)

        elif self.operador == Operador.DIV:
            if nodoIzq in [Types.INT64, Types.FLOAT64]:
                if nodoDer in [Types.INT64, Types.FLOAT64]:
                    return self.exp1.getValor(driver, ts) / self.exp2.getValor(driver, ts)
                else:
                    print(f'La 2da expresion de la division debe ser un integer o float ', self.exp2.linea,
                          self.exp2.columna)
            else:
                print(f'La 1er expresion de la division debe ser un integer o float', self.exp2.linea,
                      self.exp2.columna)

        else:
            print(f'La operacion {self.operador} no es soportado')