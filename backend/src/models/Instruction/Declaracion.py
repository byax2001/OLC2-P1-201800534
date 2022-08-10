from models.Instruction.Instruction import Instruccion
from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos,getTipo
from models.TablaSymbols.Symbol import Symbol

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
            existe=ts.buscarActualTs(self.id);
            if(existe==None):
                if(self.tipoVar==None):
                    newVar=Symbol(self.mut,self.id,v_exp,0,t_exp,self.linea,self.columna)
                    ts.addVar(self.id,newVar)
                    print("se añadio una variable")
                else:
                    if(self.tipoVar==t_exp):
                        newVar = Symbol(self.mut, self.id, v_exp, 0, t_exp, self.linea, self.columna)
                        ts.addVar(self.id, newVar)
                        print("se añadio una variable")
                    else:
                        print("El tipo de variable no corresponde con el valor de la variable a declarar")
            else:
                print("La variable ya ha sido declarada con anterioridad")
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
        elif (tipo==Tipos.STRING):
            return ""
        elif (tipo==Tipos.CHAR):
            return "\0"
