from models.Abstract.Instruction import Instruccion
from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.Tipos import Tipos,getTipo
from models.TablaSymbols.Symbol import Symbol
from models.TablaSymbols.SymC3d import SymC3d
from models.Expresion.Vector.Vector import Vector
from models.TablaSymbols.ValC3d import ValC3d
from BaseDatos.B_datos import B_datos

class Declaracion(Instruccion):
    def __init__(self,mut:bool,id:str,tipo:str, exp: Expresion, linea:int, columna:int):
        super().__init__()
        self.mut=mut
        self.id=id
        self.tipoVar=getTipo(tipo) if tipo!="" else None
        self.exp = exp
        self.linea = linea
        self.columna = columna
        self.tacceso = 0

    def ejecutar(self, driver, ts):
        if (self.exp != None):
            t_exp=self.exp.getTipo(driver,ts)
            v_exp=self.exp.getValor(driver,ts)
            if t_exp != Tipos.ERROR:
                existe=ts.buscarActualTs(self.id);
                if(existe==None):
                    if self.tipoVar==None: #si no se declaro el tipo de variable
                        if t_exp==Tipos.STRUCT:
                            newVar = Symbol(mut=self.mut, id=self.id, value=v_exp, tipo_simbolo=4, tipo=t_exp,
                                            line=self.linea, column=self.columna, tacceso=self.tacceso)
                            ts.addVar(self.id, newVar)
                            print("se añadio una variable Struc")
                            B_datos().appendVar(id=self.id, t_simbolo=newVar.tsimbolo, t_dato=newVar.tipo,
                                                ambito=ts.env, fila=self.linea, columna=self.columna)
                        elif type(v_exp)!=list:
                            newVar=Symbol(mut=self.mut,id=self.id,value=v_exp,tipo_simbolo=0,tipo=t_exp,
                                          line=self.linea,column=self.columna, tacceso=self.tacceso)

                            ts.addVar(self.id,newVar) #se añadio variable y la funcion devolvio la posicion de la variable en el stack

                            print("se añadio una variable")
                            B_datos().appendVar(id=self.id, t_simbolo=newVar.tsimbolo, t_dato=newVar.tipo, ambito=ts.env,
                                              fila=self.linea,
                                              columna=self.columna)
                        else:  #si lo que se manda es la parte de un arreglo o vector
                            # let p=[[1,2,3],[2,4,5]]  - declaracion de arreglo (ya existe instruccion a parte para eso)
                            # let a=p[0] - declaracion normal con una posicion de un arreglo que da un array
                            nvector = Vector(vec=v_exp, stateCap=False, capacity=0)
                            symbol = Symbol(mut=self.mut, id=self.id, value=nvector, tipo_simbolo=1, tipo=t_exp,
                                            line=self.linea, column=self.columna, tacceso=self.tacceso)
                            ts.addVar(self.id, symbol)
                            print("Arreglo declarado")
                            B_datos().appendVar(id=self.id, t_simbolo=symbol.tsimbolo, t_dato=symbol.tipo, ambito=ts.env,
                                              fila=self.linea,
                                              columna=self.columna)
                    else: #si si se declaro el tipo de variable
                        if(self.tipoVar==t_exp):#el tipo de variable y la expresion a asignar deben de ser del mismo tipo para que sea posible declararlas
                            if type(v_exp) != list:
                                newVar = Symbol(mut=self.mut,id=self.id, value=v_exp, tipo_simbolo=0,tipo= t_exp,
                                                line= self.linea,column= self.columna, tacceso=self.tacceso)

                                ts.addVar(self.id, newVar)
                                print("se añadio una variable")

                                B_datos().appendVar(id=self.id, t_simbolo=newVar.tsimbolo, t_dato=newVar.tipo,
                                                  ambito=ts.env,
                                                  fila=self.linea,
                                                  columna=self.columna)
                            else: #si lo que se manda es la parte de un arreglo o vector
                                nvector = Vector(vec=v_exp, stateCap=False, capacity=0)
                                symbol = Symbol(mut=self.mut, id=self.id, value=nvector, tipo_simbolo=1, tipo=t_exp,
                                                line=self.linea, column=self.columna, tacceso=self.tacceso)
                                ts.addVar(self.id, symbol)
                                print("Arreglo declarado")
                                B_datos().appendVar(id=self.id, t_simbolo=symbol.tsimbolo, t_dato=symbol.tipo,
                                                  ambito=ts.env,
                                                  fila=self.linea,
                                                  columna=self.columna)
                        elif self.tipoVar==Tipos.USIZE and t_exp==Tipos.INT64 and v_exp>=0: #Unica excepcion donde el tipo de variable y tipo de expresion son diferentes y posibles de declarar
                            newVar = Symbol(mut=self.mut, id=self.id, value=v_exp, tipo_simbolo=0, tipo=Tipos.USIZE,
                                            line=self.linea, column=self.columna, tacceso=self.tacceso)
                            ts.addVar(self.id, newVar)
                            print("se añadio una variable")
                            B_datos().appendVar(id=self.id, t_simbolo=newVar.tsimbolo, t_dato=newVar.tipo, ambito=ts.env,
                                              fila=self.linea,
                                              columna=self.columna)
                        else:
                            print(f"El tipo de variable no corresponde con el valor de la variable a declarar {self.linea}")
                            error = "El tipo de variable no corresponde con el valor de la variable a declarar "
                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                              columna=self.columna)
                            return False
                else:
                    print("La variable ya ha sido declarada con anterioridad")
                    error = "La variable ya ha sido declarada con anterioridad"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                      columna=self.columna)
                    return False
            else:
                print("La expresion para declarar retorna un valor con error")
                error = "La expresion para declarar retorna un valor con error"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                  columna=self.columna)
                return False
        else:
            existe = ts.buscarActualTs(self.id)
            v_exp = Declaracion.valueDefault(self.tipoVar)
            t_exp = self.tipoVar
            if (existe == None):
                newVar = Symbol(self.mut, self.id, v_exp, 0, t_exp, self.linea, self.columna)
                ts.addVar(self.id, newVar)
            else:
                print("La variable ya ha sido declarada con anterioridad")
                error = "La variable ya ha sido declarada con anterioridad"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                  columna=self.columna)
                return False

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
    def getId(self):
        return self.id
    def getExp(self):
        return self.exp
    def changeAcces(self,acceso:int):
        self.tacceso=acceso

    def generarC3d(self,ts:Enviroment,ptr:int):
        symbol=ts.buscarActualTs(self.id)
        if symbol==None:
            self.exp.generator = self.generator

            newValue: ValC3d = self.exp.generarC3d(ts=ts,ptr=ptr)
            newVar = Symbol(mut=self.mut, id=self.id, value=newValue.valor, tipo_simbolo=0, tipo=newValue.tipo,
                            line=self.linea, column=self.columna, tacceso=self.tacceso)

            temp_var: SymC3d = ts.addVar(self.id, newVar) #----------------------------

            if (temp_var.tipo != Tipos.BOOLEAN):
                self.generator.addSetStack(str(temp_var.position), newValue.getValue()) #Stack[(int)pos]= val
            else:
                #Aqui no estoy añadiendo directamente el valor al hacer el addSetStack
                # sino escribiendo un if que dependiendo del resultado anterior asignara 1 o 0 a la variable
                #ejem:  if (valor==True){ var1=1  } else {var1=0}:
                    # con el if realizado en anteriores expresiones, se ira al label que asigna 1 o 0 (true o false)
                    # en el stack y no tocara el otro

                newLabel = self.generator.newLabel()  # metodo que crea y retorna un label  Ln, esta es la etiqueta de salida
                self.generator.addLabel(newValue.trueLabel)  # añade Ln:  ya existente al codigo principal (true)
                self.generator.addSetStack(str(temp_var.position), '1')   #Stack[(int)num]= 1
                self.generator.addGoto(newLabel) #goto Ln ;
                self.generator.addLabel(newValue.falseLabel) # añade Ln:  ya existente al codigo principal (false)
                self.generator.addSetStack(str(temp_var.position), '0')  #Stack[(int)num]= 0
                self.generator.addLabel(newLabel) # añade Ln:  ya existente al codigo principal

                # if var==1 goto L1
                # goto L2
                # L1:
                #  var1= 1
                # goto   LnewLabel
                # L2:
                #   var1= 0
                # LnewLabel:
        else:
            print("Variable ya declarada")