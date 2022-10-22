from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Symbol import Symbol,Symbols
from models.TablaSymbols.Enviroment import Enviroment
from models.Expresion.Vector.Vector import Vector
from models.TablaSymbols.ValC3d import ValC3d

class Id(Expresion):    
    def __init__(self, id:str, linea: int, columna: int):
        super().__init__()
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

    def generarC3d(self,ts:Enviroment,ptr:int):
        self.generator.addComment(f"ID EXPRESION: {self.id}")
        ts.generator =self.generator
        tmp_aux = self.generator.newTemp() #para volver al enviroment actual de la pila luego del proceso de busqueda, y resta de P
        symbol:Symbol = ts.buscarC3d(self.id,tmp_aux,self.en_funcion)
        result = ValC3d(valor="0",isTemp=False,tipo=Tipos.ERROR)
        if symbol!=None:
            if self.paso_parametro == False: #CUANDO LO PIDEN SIN &
                if symbol.paso_parametro == False:
                    tmpR= self.generator.newTemp()
                    index = self.generator.newTemp()
                    self.generator.addBackStack(index=tmp_aux)  # para retroceder entre enviroments
                    self.generator.addExpression(target=index,left="P",right=str(symbol.position),operator="+")
                    self.generator.addNextStack(tmp_aux)  # volver al enviroment actual de la pila
                    self.generator.addGetStack(target=tmpR, index=index)

                else: #SE DECLARO COMO PASO DE PARAMETRO EL SIMBOLO pero se requiere su valor
                      #SE SACA PRIMERO EL VALOR DE DIRECCION EN EL STACK Y CON ESE VALOR SE SACA EL VALOR REQUERIO
                    tmpR = self.generator.newTemp()
                    index = self.generator.newTemp()
                    self.generator.addBackStack(index=tmp_aux)  # para retroceder entre enviroments
                    self.generator.addExpression(target=index, left="P", right=str(symbol.position), operator="+")
                    self.generator.addNextStack(tmp_aux)  # volver al enviroment actual de la pila
                    self.generator.addGetStack(target=tmpR, index=index)
                    self.generator.addGetStack(target=tmpR, index=tmpR)
                if symbol.tsimbolo == Symbols.ARREGLO:
                    result.tipo_aux = Tipos.ARREGLO
                    result.prof_array = symbol.value.profundidad
                elif symbol.tsimbolo == Symbols.VECTOR:
                    result.tipo_aux = Tipos.VECTOR
                    result.prof_array = symbol.value.profundidad

                if symbol.tipo != Tipos.BOOLEAN or symbol.tsimbolo == Symbols.VECTOR or symbol.tsimbolo == Symbols.ARREGLO:
                    result.valor = tmpR
                    result.isTemp = True
                    result.tipo = symbol.tipo
                else:
                    valor_r = ValC3d(valor="", isTemp=False, tipo=Tipos.BOOLEAN)
                    if (self.trueLabel == ""):
                        self.trueLabel = self.generator.newLabel()
                    if (self.falseLabel == ""):
                        self.falseLabel = self.generator.newLabel()
                    self.generator.addIf(tmpR, "1", "==", self.trueLabel)
                    self.generator.addGoto(self.falseLabel)

                    valor_r.trueLabel = self.trueLabel
                    valor_r.falseLabel = self.falseLabel
                    result = valor_r
            else:#CUANDO LO PIDEN CON &
                if symbol.paso_parametro == False:#fue declarado de forma normal
                    tmpR = self.generator.newTemp()
                    self.generator.addBackStack(index=tmp_aux)  # para retroceder entre enviroments
                    self.generator.addExpression(target=tmpR, left="P", right=str(symbol.position), operator="+")
                    self.generator.addNextStack(tmp_aux)  # volver al enviroment actual de la pila
                    tmpR=f"(int){tmpR}"
                else: #si el simbolo fue declarado como un paso de parametro
                    #SI EL SIMBOLO FUE DECLARADO COMO PASO DE PARAMETRO LO QUE SE GUARDO EN LA PILA: STACK[index] = val
                    #FUE LA DIRECCION MANDADA, ENTONCES ES DE SUBSTRAER DICHA DIRECCION DE LA PILLA
                    tmpR = self.generator.newTemp()
                    index = self.generator.newTemp()
                    self.generator.addBackStack(index=tmp_aux)  # para retroceder entre enviroments
                    self.generator.addExpression(target=index, left="P", right=str(symbol.position), operator="+")
                    self.generator.addNextStack(tmp_aux)  # volver al enviroment actual de la pila
                    self.generator.addGetStack(target=tmpR, index=index)
                if symbol.tsimbolo == Symbols.ARREGLO:
                    result.tipo_aux = Tipos.ARREGLO
                    result.prof_array = symbol.value.profundidad
                elif symbol.tsimbolo == Symbols.VECTOR:
                    result.tipo_aux = Tipos.VECTOR
                    result.prof_array = symbol.value.profundidad

                result.valor = tmpR
                result.isTemp = True
                result.tipo = symbol.tipo
        else:
            error = f"no existe dicha id {self.id}"
            print(error)

        return result