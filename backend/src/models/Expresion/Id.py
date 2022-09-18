from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Symbol import Symbol
from models.TablaSymbols.Enviroment import Enviroment
from models.Expresion.Vector.Vector import Vector
from models.TablaSymbols.ValC3d import ValC3d

class Id(Expresion):    
    def __init__(self, id:str, linea: int, columna: int):
        self.tipo=None
        self.value=None
        self.id = id
        self.linea = linea
        self.columna = columna

    def getTipo(self, driver, ts):
        symbol = ts.buscar(self.id);
        if symbol != None:
            self.tipo = symbol.tipo
        else:
            self.tipo =Tipos.ERROR
        return self.tipo


    def getValor(self, driver, ts:Enviroment):
        symbol = ts.buscar(self.id);
        if symbol!=None:
            self.value = symbol.value
            if isinstance(self.value,Vector):  #EN CASO SEA UN ARRAY LO LLAMADO ESTE ESTARA ADENTRO DE UNA CLASE VECTOR
                self.value=self.value.vector   #CON LA VARIABLE VECTOR (EL VALOR DESEADO A USAR) Y OTROS PARAMETROS
            return self.value
        else:
            return None
    def getVector(self,driver,ts:Enviroment):
        symbol = ts.buscar(self.id);
        if symbol != None:
            self.value = symbol.value
            return self.value
        else:
            return None
    def getSymbol(self,driver,ts:Enviroment):
        symbol = ts.buscar(self.id);
        if symbol != None:
            return symbol
        else:
            return None
    def ejecutar(self, driver, ts):
        """En la mayoria de expresiones no realiza nada"""
        pass

    def generarC3d(self,ts,ptr:int):
        symbol:Symbol = ts.buscar(self.id)
        if symbol!=None:
            newTemp = self.generator.newTemp()

            self.generator.addGetStack(newTemp, str(symbol.position))

            if (symbol.tipo != Tipos.BOOLEAN):
                return ValC3d(valor=newTemp,isTemp= True,tipo= symbol.tipo)
            else:
                val = ValC3d(valor="",isTemp= False,tipo= Tipos.BOOLEAN)

                if (self.trueLabel == ""):
                    self.trueLabel = self.generator.newLabel()

                if (self.falseLabel == ""):
                    self.falseLabel = self.generator.newLabel()

                self.generator.addIf(newTemp, "1", "==", self.trueLabel)
                self.generator.addGoto(self.falseLabel)

                val.trueLabel = self.trueLabel
                val.falseLabel = self.falseLabel

                return val
        else:
            print("no existe dicha id")