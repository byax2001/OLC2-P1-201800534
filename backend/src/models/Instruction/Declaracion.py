from models.Abstract.Instruction import Instruccion
from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.Tipos import Tipos,getTipo
from models.TablaSymbols.Symbol import Symbol,Symbols
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
        #DECLARACION CON PASO DE PARAMETRO
        self.dec_paso_parametro = False

        # cambio de entorno
        self.puntero_entorno_nuevo=""
        self.en_funcion=False

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
        self.generator.addComment(f"Declaracion var: {self.id}")
        symbol=ts.buscarActualTs(self.id)
        if symbol==None:
            self.exp.generator = self.generator
            exp_dec: ValC3d = self.exp.generarC3d(ts=ts, ptr=ptr)
            if self.tipoVar == None:
                self.declarar_c3d(ts,ptr,exp_dec)
            else:
                if self.tipoVar==exp_dec.tipo or (self.tipoVar in [Tipos.INT64,Tipos.USIZE] and exp_dec.tipo in [Tipos.INT64,Tipos.USIZE]):
                    self.declarar_c3d(ts,ptr,exp_dec)
                else:
                    error="Tipo de variable no corresponde con el valor a declarar"
                    print(error)
        else:
            print("Variable ya declarada")

    def declarar_c3d(self,ts,ptr,exp:ValC3d):

        newVar = Symbol(mut=self.mut, id=self.id, value=exp.valor, tipo_simbolo=0, tipo=exp.tipo,
                        line=self.linea, column=self.columna, tacceso=self.tacceso,position=ts.size)
        newVar.paso_parametro=self.dec_paso_parametro
        temp_var: SymC3d = ts.addVar(self.id, newVar)  # ----------------------------
        aux_index = self.generator.newTemp()  # tendra el index
        self.generator.addComment("Ingreso a la Pila")
        Puntero ="P"
        if self.en_funcion: #EN EL CASO SEA UNA DECLARACION ANTES DE LLAMAR A UNA FUNCION SE CAMBIA EL TIPO DE PUNTERO
                            # DE P   a   tn   (tn=P+ts.size)
            Puntero = self.puntero_entorno_nuevo

        if temp_var.tipo != Tipos.BOOLEAN or exp.tipo_aux == Tipos.ARREGLO or exp.tipo_aux == Tipos.VECTOR:
            self.generator.addExpression(target=aux_index, left=Puntero, right=str(temp_var.position), operator="+")
            self.generator.addSetStack(index=aux_index, value=str(temp_var.valor))  # Stack[(int)pos]= val
        else:
            # Aqui no estoy añadiendo directamente el valor al hacer el addSetStack
            # sino escribiendo un if que dependiendo del resultado anterior asignara 1 o 0 a la variable
            # ejem:  if (valor==True){ var1=1  } else {var1=0}:
            # con el if realizado en anteriores expresiones, se ira al label que asigna 1 o 0 (true o false)
            # en el stack y no tocara el otro

            newLabel = self.generator.newLabel()  # metodo que crea y retorna un label  Ln, esta es la etiqueta de salida
            self.generator.addLabel(exp.trueLabel)  # añade Ln:  ya existente al codigo principal (true)
            self.generator.addExpression(target=aux_index, left=Puntero, right=str(temp_var.position), operator="+")
            self.generator.addSetStack(index=aux_index, value='1')  # Stack[(int)num]= 1
            self.generator.addGoto(newLabel)  # goto Ln ;
            self.generator.addLabel(exp.falseLabel)  # añade Ln:  ya existente al codigo principal (false)
            self.generator.addExpression(target=aux_index, left=Puntero, right=str(temp_var.position), operator="+")
            self.generator.addSetStack(index=aux_index, value='0')  # Stack[(int)num]= 0
            self.generator.addLabel(newLabel)  # añade Ln:  ya existente al codigo principal

            # if var==1 goto L1
            # goto L2
            # L1:
            #  var1= 1
            # goto   LnewLabel
            # L2:
            #   var1= 0
            # LnewLabel:
    def decStructsC3d(self,ts,ptr):
        self.generator.addComment(f"Declaracion var struct: {self.id}")
        symbol = ts.buscarActualTs(self.id)
        if symbol == None:
            self.exp.generator = self.generator
            exp_dec: ValC3d = self.exp.generarC3d(ts=ts, ptr=ptr)
            if self.tipoVar == None:
                self.declarar_elementos_structC3d(ts, ptr, exp_dec)
            else:
                if self.tipoVar == exp_dec.tipo or (
                        self.tipoVar in [Tipos.INT64, Tipos.USIZE] and exp_dec.tipo in [Tipos.INT64, Tipos.USIZE]):
                    self.declarar_elementos_structC3d(ts, ptr, exp_dec)
                else:
                    error = "Tipo de variable no corresponde con el valor a declarar"
                    print(error)
        else:
            print("Variable ya declarada")

    def declarar_elementos_structC3d(self,ts,ptr,exp:ValC3d):
        tipoSym= 0
        if exp.tipo_aux == Tipos.ARREGLO:
            tipoSym= 1
        elif exp.tipo_aux == Tipos.VECTOR:
            tipoSym=3

        newVar = Symbol(mut=self.mut, id=self.id, value=exp.valor, tipo_simbolo=tipoSym, tipo=exp.tipo,
                        line=self.linea, column=self.columna, tacceso=self.tacceso, position=ts.size)
        newVar.paso_parametro = self.dec_paso_parametro
        temp_var: SymC3d = ts.addVar(self.id, newVar)  # ----------------------------
        aux_index = self.generator.newTemp()  # tendra el index
        self.generator.addComment("Ingreso al Heap por el puntero")
        Puntero = ptr #ptr tiene el puntero en este caso

        if temp_var.tipo != Tipos.BOOLEAN or exp.tipo_aux == Tipos.ARREGLO or exp.tipo_aux == Tipos.VECTOR:
            self.generator.addExpression(target=aux_index, left=Puntero, right=str(temp_var.position), operator="+")
            self.generator.addSetHeap(index=aux_index, value=str(temp_var.valor))  # Heap[(int)pos]= val
        else:
            # Aqui no estoy añadiendo directamente el valor al hacer el addSetStack
            # sino escribiendo un if que dependiendo del resultado anterior asignara 1 o 0 a la variable
            # ejem:  if (valor==True){ var1=1  } else {var1=0}:
            # con el if realizado en anteriores expresiones, se ira al label que asigna 1 o 0 (true o false)
            # en el stack y no tocara el otro

            newLabel = self.generator.newLabel()  # metodo que crea y retorna un label  Ln, esta es la etiqueta de salida
            self.generator.addLabel(exp.trueLabel)  # añade Ln:  ya existente al codigo principal (true)
            self.generator.addExpression(target=aux_index, left=Puntero, right=str(temp_var.position), operator="+")
            self.generator.addSetHeap(index=aux_index, value='1')  # Heap[(int)num]= 1
            self.generator.addGoto(newLabel)  # goto Ln ;
            self.generator.addLabel(exp.falseLabel)  # añade Ln:  ya existente al codigo principal (false)
            self.generator.addExpression(target=aux_index, left=Puntero, right=str(temp_var.position), operator="+")
            self.generator.addSetHeap(index=aux_index, value='0')  # Heap[(int)num]= 0
            self.generator.addLabel(newLabel)  # añade Ln:  ya existente al codigo principal

            # if var==1 goto L1
            # goto L2
            # L1:
            #  var1= 1
            # goto   LnewLabel
            # L2:
            #   var1= 0
            # LnewLabel: