from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import definirTipo,Tipos,getTipo


class Primitivo(Expresion):
    def __init__(self, valor, linea: int, columna: int, aux = ""):
        self.tipo = None if aux=="" else getTipo(aux)
        self.value = valor
        self.linea = linea
        self.columna = columna

    def getTipo(self, driver, ts):
        if self.tipo is None:
            value = self.getValor(driver, ts)
            return definirTipo(value)
        else:
            return self.tipo

    def getValor(self, driver, ts):
        value = self.value
        self.tipo = definirTipo(value)
        if(self.tipo==Tipos.STRING or self.tipo==Tipos.CHAR or self.tipo==Tipos.STR):
            value = Primitivo.limpCad(value)
        return value

    def limpCad(cadena:str):
        cadena=cadena[1:len(cadena)-1]
        cadena=cadena.replace("\\\"","\"")
        cadena=cadena.replace("\\n","\n")
        cadena=cadena.replace("\\t","\t")
        cadena=cadena.replace("\\r","\r")
        cadena = cadena.replace("\\\'", "\'")
        cadena=cadena.replace("\\\\","\\")
        return cadena
    def ejecutar(self, driver, ts):
        """En la mayoria de expresiones no realiza nada"""
        pass
