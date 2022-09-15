from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import definirTipo,Tipos,getTipo
from models.TablaSymbols.Value import Value
from models.TablaSymbols.ValC3d import ValC3d

class Primitivo(Expresion):
    def __init__(self, valor, linea: int, columna: int, aux = ""):
        super().__init__()
        self.tipo = None if aux=="" else getTipo(aux)
        self.value = valor
        self.linea = linea
        self.columna = columna
        self.instancia=0

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

        if self.tipo is None:
            self.tipo = definirTipo(self.value)
        if (self.tipo == Tipos.STRING or self.tipo == Tipos.CHAR or self.tipo == Tipos.STR):
            _value = self.value
            _value = Primitivo.limpCad(_value)
        value = Value(valor=_value, isTemp=True, tipo=self.tipo)
        return value


    def generarC3d(self,ts,ptr:int):
        if self.tipo is None:
            self.tipo=definirTipo(self.value)

        if self.tipo==Tipos.INT64 or self.tipo==Tipos.FLOAT64:
            return ValC3d(valor=str(self.value),isTemp=False,tipo=self.tipo)
        elif self.tipo==Tipos.STR or self.tipo==Tipos.CHAR:
            newTemp = self.generator.newTemp()  #   = tnum
            self.generator.addExpression(newTemp, "H", "", "")   #  en este caso : tnum = H;
            for char in self.value:
                self.generator.addSetHeap("H", str(ord(char)))  # heap[(int)num]=   ascii code
                self.generator.addNextHeap() #H = H + 1

            self.generator.addSetHeap("H", "-1") # heap[(int)num]= -1
            return ValC3d(str(newTemp), True, self.tipo)
        elif self.tipo== Tipos.BOOLEAN:
            if self.value==True:
                valor = "1"
            else:
                valor = "0"
            val = ValC3d("", False, Tipos.BOOLEAN)

            if (self.trueLabel == ""):
                self.trueLabel = self.generator.newLabel()  #Ln: (true)

            if (self.falseLabel == ""):
                self.falseLabel = self.generator.newLabel()  #Ln+1: (false)
                                  #li   ld   operador
            self.generator.addIf(valor, "1", "==", self.trueLabel)  # if (valor==1) goto Ln (true)
            self.generator.addGoto(self.falseLabel) # goto Ln+1 (false)

            val.trueLabel = self.trueLabel
            val.falseLabel = self.falseLabel


            return val


def resetInst(self):
        if self.instancia>1:
            self.instancia=0
            self.value=None
            self.tipo=None