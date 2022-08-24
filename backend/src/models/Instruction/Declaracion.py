from models.Instruction.Instruction import Instruccion
from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos,getTipo
from models.TablaSymbols.Symbol import Symbol
from models.Expresion.Vector.Vector import Vector

class Declaracion(Instruccion):
    def __init__(self,mut:bool,id:str,tipo:str, exp: Expresion, linea:int, columna:int):
        self.mut=mut
        self.id=id
        self.tipoVar=getTipo(tipo) if tipo!="" else None
        self.exp = exp
        self.linea = linea
        self.columna = columna


    def ejecutar(self, driver, ts):
        if (self.exp != None):
            t_exp=self.exp.getTipo(driver,ts)
            v_exp=self.exp.getValor(driver,ts)
            if t_exp != Tipos.ERROR:
                existe=ts.buscarActualTs(self.id);
                if(existe==None):
                    if(self.tipoVar==None):
                        if type(v_exp)!=list:
                            newVar=Symbol(mut=self.mut,id=self.id,value=v_exp,tipo_simbolo=0,tipo=t_exp,line=self.linea,column=self.columna)
                            ts.addVar(self.id,newVar)
                            print("se añadio una variable")
                        else:  #si lo que se manda es la parte de un arreglo o vector
                            nvector = Vector(vec=v_exp, stateCap=False, capacity=0)
                            symbol = Symbol(mut=self.mut, id=self.id, value=nvector, tipo_simbolo=1, tipo=t_exp,
                                            line=self.line, column=self.column)
                            ts.addVar(self.id, symbol)
                            print("Arreglo declarado")
                    else:
                        if(self.tipoVar==t_exp):
                            if type(v_exp) != list:
                                newVar = Symbol(mut=self.mut,id=self.id, value=v_exp, tipo_simbolo=0,tipo= t_exp, line= self.linea,column= self.columna)
                                ts.addVar(self.id, newVar)
                                print("se añadio una variable")
                            else: #si lo que se manda es la parte de un arreglo o vector
                                nvector = Vector(vec=v_exp, stateCap=False, capacity=0)
                                symbol = Symbol(mut=self.mut, id=self.id, value=nvector, tipo_simbolo=1, tipo=t_exp,
                                                line=self.line, column=self.column)
                                ts.addVar(self.id, symbol)
                                print("Arreglo declarado")
                        else:
                            print("El tipo de variable no corresponde con el valor de la variable a declarar")
                else:
                    print("La variable ya ha sido declarada con anterioridad")
            else:
                print("La expresion para declarar retorna un valor con error")
        else:
            existe = ts.buscarActualTs(self.id)
            v_exp = Declaracion.valueDefault(self.tipoVar)
            t_exp = self.tipoVar
            if (existe == None):
                newVar = Symbol(self.mut, self.id, v_exp, 0, t_exp, self.linea, self.columna)
                ts.addVar(self.id, newVar)
            else:
                print("La variable ya ha sido declarada con anterioridad")

        #REVISAR SI EN EL PROYECTO HAY DECLARACIONES   let A; let B;
        #EN ESE CASO CREAR METODO QUE DEVUELVA UN VALOR POR DEFAULT EN CADA TIPO DE VARIABLE PARA DARSELOS COMO VALOR
    def valueDefault(self, tipo:Tipos):
        if(tipo==Tipos.INT64):
            return 0
        elif(tipo==Tipos.FLOAT64):
            return 0.0
        elif (tipo==Tipos.BOOLEAN):
            return False
        elif (tipo==Tipos.STR):
            return ""
        elif (tipo==Tipos.STRING):
            return ""
        elif (tipo==Tipos.CHAR):
            return "\0"
    #metodo para hacer declaraciones luego de llamada una funcion
    def changeExp(self,exp:Expresion):
        self.exp=exp