from models.Expresion.Operacion.Operacion import Operacion, Operador, getOperacion
from models.TablaSymbols.Tipos import Tipos,definirTipo
import math
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d

class Aritmeticas(Operacion): #de esta forma se esta indicando que aritmeticas hereda de Operacion
    #var Operacion: exp1: Expresion, operador, exp2: Expresion, linea, columna, expU
    #ARITMETICAS TIENE UN CONSTRUCTOR HEREDADO POR "OPERACION"
    def getTipo(self, driver, ts):
        self.resetInst()
        if self.tipo==None and self.value==None:
            self.getValor(driver,ts)
            if self.value==None:
                self.tipo=Tipos.ERROR
        else:
            self.instancia+=1
        return self.tipo

    # get valor con condicionales
    def getValor(self, driver, ts):
        self.instancia+=1
        if self.value==None and self.tipo==None:
            t_nodoIzq = self.exp1.getTipo(driver, ts)
            t_nodoDer = self.exp2.getTipo(driver, ts) if not self.expU else None

            if self.expU ==True:
                self.value= - self.exp1.getValor(driver, ts)
                self.tipo=definirTipo(self.value)
                return self.value

            valorizq = self.exp1.getValor(driver, ts)
            valorder = self.exp2.getValor(driver, ts)
            if self.operador == Operador.SUMA:
                # INT + ?
                # FLOAT + ?
                if t_nodoIzq == t_nodoDer:
                    if t_nodoIzq in [Tipos.INT64, Tipos.FLOAT64]:
                        self.value= valorizq + valorder
                        self.tipo = definirTipo(self.value)
                elif t_nodoIzq in [Tipos.INT64, Tipos.USIZE] and t_nodoDer in [Tipos.INT64, Tipos.USIZE]:
                    self.value= valorizq + valorder
                    self.tipo = definirTipo(self.value)
                elif t_nodoIzq==Tipos.STRING and t_nodoDer==Tipos.STR:
                    self.value= str(valorizq) +str(valorder)
                    self.tipo = Tipos.STRING
                else:
                    print(f'Los nodos no son del mismo valor o no son posible de concatenar o sumar', self.exp2.linea,
                            self.exp2.columna)
                    error = "Los nodos no son del mismo valor o no son posible de concatenar o sumar"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                      columna=self.columna)
            elif self.operador == Operador.RESTA:
                if t_nodoIzq == t_nodoDer:
                    if t_nodoIzq in [Tipos.INT64, Tipos.FLOAT64]:
                        self.value= valorizq - valorder
                        self.tipo = definirTipo(self.value)
                    else:
                        print(f'Las expresiones para la resta deben de ser un integer, float o usize ', self.exp2.linea, self.exp2.columna)
                        error = "Las expresiones para la resta deben de ser un integer, float o usize"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                          columna=self.column)
                elif t_nodoIzq in [Tipos.INT64, Tipos.USIZE] and t_nodoDer in [Tipos.INT64, Tipos.USIZE]:
                    self.value= valorizq - valorder
                    self.tipo = definirTipo(self.value)
                else:
                    print(f'Las expresiones a restar deben de ser del mismo  {self.exp1.linea}')
                    error = "Las expresiones a restar deben de ser del mismo"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                      columna=self.columna)
            elif self.operador == Operador.MULTI:
                if t_nodoIzq == t_nodoDer:
                    if t_nodoIzq in [Tipos.INT64, Tipos.FLOAT64]:
                        self.value= valorizq * valorder
                        self.tipo = definirTipo(self.value)
                    else:
                        print(f'Las expresiones para la  multiplicacion debe ser un integer o float ', self.exp2.linea, self.exp2.columna)
                        error = "Las expresiones para la  multiplicacion debe ser un integer o float"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                          columna=self.columna)
                elif t_nodoIzq in [Tipos.INT64, Tipos.USIZE] and t_nodoDer in [Tipos.INT64, Tipos.USIZE]:
                    self.value= valorizq * valorder
                    self.tipo = definirTipo(self.value)

                else:
                   print(f'Las expresiones a multiplicar deben de ser del mismo tipo')
                   error = "Las expresiones a multiplicar deben de ser del mismo tipo"
                   B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                     columna=self.columna)
            elif self.operador == Operador.DIV:
                if t_nodoIzq == t_nodoDer:
                    v_exp1 = valorizq
                    v_exp2 = valorder
                    if v_exp2!=0:
                        if t_nodoIzq==Tipos.INT64:
                            self.value= math.trunc(v_exp1/ v_exp2)
                            self.tipo = definirTipo(self.value)
                        elif t_nodoIzq ==Tipos.FLOAT64:
                            self.value= v_exp1 / v_exp2
                            self.tipo = definirTipo(self.value)
                        else:
                            print(f'Las expresiones para la  division debe ser un integer o float ', self.exp2.linea, self.exp2.columna)
                            error = "Las expresiones para la  division debe ser un integer o float"
                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                              columna=self.columna)
                    else:
                        print("Error: Se intenta dividir entre 0")
                        error = "Error: Se intenta dividir entre 0"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                          columna=self.columna)
                elif t_nodoIzq in [Tipos.INT64, Tipos.USIZE] and t_nodoDer in [Tipos.INT64, Tipos.USIZE]:
                    v_exp1 = valorizq
                    v_exp2 = valorder
                    if v_exp2!=0:
                        self.value= math.trunc(v_exp1/ v_exp2)
                        self.tipo = definirTipo(self.value)
                    else:
                        print("Error: Se intenta dividir entre 0")
                        error = "Error: Se intenta dividir entre 0"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                          columna=self.columna)
                else:
                   print(f'Las expresiones a dividir deben de ser del mismo tipo')
                   error = "Las expresiones a dividir deben de ser del mismo tipo"
                   B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                     columna=self.columna)
            elif self.operador == Operador.MOD:
                if t_nodoIzq == t_nodoDer:
                    if t_nodoIzq==Tipos.INT64:
                        self.value= valorizq % valorder
                        self.tipo = definirTipo(self.value)
                    elif t_nodoIzq==Tipos.FLOAT64:
                        self.value= float(valorizq % valorder)
                        self.tipo = definirTipo(self.value)
                    else:
                        print(f'Las expresiones para usar el operador modulo debe ser un integer o float ', self.exp2.linea, self.exp2.columna)
                        error = "Las expresiones para usar el operador modulo debe ser un integer o float"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                          columna=self.columna)
                elif t_nodoIzq in [Tipos.INT64, Tipos.USIZE] and t_nodoDer in [Tipos.INT64, Tipos.USIZE]:
                    self.value= valorizq % valorder
                    self.tipo = definirTipo(self.value)
                else:
                   print(f'Las expresiones a hacer mod deben de ser del mismo tipo')
                   error = "Las expresiones a hacer mod deben de ser del mismo tipo"
                   B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                     columna=self.columna)
            elif self.operador == Operador.POW:
                if t_nodoIzq == t_nodoDer:
                    if t_nodoIzq ==Tipos.INT64:
                        self.value= pow(valorizq,valorder)
                        self.tipo = definirTipo(self.value)
                    else:
                        print(f'Las expresiones para el operador pow debe ser un integer ', self.exp2.linea, self.exp2.columna)
                        error = "Las expresiones para el operador pow debe ser un integer"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                          columna=self.columna)
                elif t_nodoIzq in [Tipos.INT64, Tipos.USIZE] and t_nodoDer in [Tipos.INT64, Tipos.USIZE]:
                    self.value= pow( valorizq, valorder )
                    self.tipo = definirTipo(self.value)
                else:
                   print(f'Las expresiones a elevar deben de ser del mismo tipo')
                   error = "Las expresiones a elevar deben de ser del mismo tipo"
                   B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                     columna=self.columna)
            elif self.operador == Operador.POWF:
                if t_nodoIzq == t_nodoDer:
                    if t_nodoIzq==Tipos.FLOAT64:
                        self.value= pow(valorizq,valorder)
                        self.tipo = definirTipo(self.value)
                    else:
                        print(f'Las expresiones para el operador powf deben de ser float ', self.exp2.linea, self.exp2.columna)
                        error = "Las expresiones para el operador powf deben de ser float "
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                          columna=self.columna)
                else:
                    print(f'Las expresiones a elevar deben de ser del mismo tipo')
                    error = "Las expresiones a elevar deben de ser del mismo tipo "
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                      columna=self.columna)
            else:
                print(f'La operacion {self.operador} no es soportado')
                error = f"La operacion {self.operador} no es soportado"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                  columna=self.columna)

        return self.value

    def resetInst(self):
        if self.instancia>1:
            self.instancia=0
            self.value=None
            self.tipo=None
    def ejecutar(self, driver, ts):
        """En la mayoria de expresiones no realiza nada"""
        pass

    def generarC3d(self,ts,ptr:int):
        self.generator.addComment("Aritmeticas")
        newTemp = self.generator.newTemp()  # = tnum Result de esta operacion
        result=ValC3d(valor=newTemp, isTemp=True, tipo=Tipos.ERROR)
        self.exp1.generator = self.generator
        if self.exp2==None and self.expU==True: #Unario: -valor
            exp1=self.exp1.generarC3d(ts,ptr)
            if exp1.tipo in [Tipos.INT64,Tipos.FLOAT64]:
                self.generator.addExpression(target=newTemp,left="",operator="-",right=exp1.valor)
                result.tipo = exp1.tipo
            return result

        if self.exp2==None:
            print("error expresion 2 es nula",end="") #imprimir sin nuevo salto de linea
            print(self.linea)
            return
        self.exp2.generator = self.generator
        exp1=self.exp1.generarC3d(ts,ptr)
        exp2=self.exp2.generarC3d(ts,ptr)

        if exp1.tipo == Tipos.STRING and exp2.tipo in [Tipos.STR,Tipos.STRING] and self.operador==Operador.SUMA:
            self.generator.addComment("Concatenacion de cadenas")
            self.generator.addExpAsign(target=newTemp,right="H")# Resultado
            self.ConcatenarStrC3d(posInit=exp1.valor)
            self.ConcatenarStrC3d(posInit=exp2.valor)
            # de ultimo añadir al heap un -1 y sumar 1 a H
            self.generator.addComment("Fin de la concatenacion")
            self.generator.addSetHeap("H", "-1")  # H
            self.generator.addNextHeap()  # H=H+1
            result.tipo = Tipos.STRING
            return result

        if exp1.tipo==exp2.tipo:
            if self.operador==Operador.SUMA:
                if exp1.tipo in [Tipos.FLOAT64,Tipos.INT64]:
                    self.generator.addExpression(target=newTemp,left=exp1.valor,operator="+",right=exp2.valor)
                    result.tipo = exp1.tipo
            elif self.operador==Operador.RESTA:
                if exp1.tipo in [Tipos.FLOAT64, Tipos.INT64]:
                    self.generator.addExpression(target=newTemp, left=exp1.valor, operator="-", right=exp2.valor)
                result.tipo=exp1.tipo
            elif self.operador==Operador.MULTI:
                if exp1.tipo in [Tipos.FLOAT64, Tipos.INT64]:
                    self.generator.addExpression(target=newTemp, left=exp1.valor, operator="*", right=exp2.valor)
                result.tipo=exp1.tipo
            elif self.operador==Operador.DIV:
                if exp1.tipo in [Tipos.FLOAT64, Tipos.INT64]:
                    self.divModC3d(exp1,exp2,newTemp,self.operador)
                result.tipo=exp1.tipo
            elif self.operador==Operador.MOD:
                if exp1.tipo in [Tipos.FLOAT64, Tipos.INT64]:
                    self.divModC3d(exp1,exp2,newTemp,self.operador)
                result.tipo = exp1.tipo
            elif self.operador==Operador.POW:
                if exp1.tipo in [Tipos.FLOAT64, Tipos.INT64]:
                    self.generator.addComment("POW----------------------")
                    tmpr=self.powC3d(exp1,exp2)
                    self.generator.addComment("POW----------------------")
                    self.generator.addExpAsign(target=newTemp,right=tmpr)

                result.tipo = exp1.tipo
            elif self.operador == Operador.POWF:
                if exp1.tipo in [Tipos.FLOAT64, Tipos.INT64]:
                    tmpr = self.powC3d(exp1, exp2)
                    self.generator.addExpAsign(target=newTemp, right=tmpr)
                result.tipo = exp1.tipo

        elif exp1.tipo in [Tipos.INT64,Tipos.USIZE] and exp2.tipo in [Tipos.INT64,Tipos.USIZE]:
            if self.operador == Operador.SUMA:
                self.generator.addExpression(target=newTemp, left=exp1.valor, operator="+", right=exp2.valor)
                result.tipo = exp1.tipo
            elif self.operador == Operador.RESTA:
                self.generator.addExpression(target=newTemp, left=exp1.valor, operator="-", right=exp2.valor)
                result.tipo = exp1.tipo
            elif self.operador == Operador.MULTI:
                self.generator.addExpression(target=newTemp, left=exp1.valor, operator="*", right=exp2.valor)
                result.tipo = exp1.tipo
            elif self.operador == Operador.DIV:
                self.divModC3d(exp1,exp2,newTemp,self.operador)
                result.tipo = exp1.tipo
            elif self.operador == Operador.MOD:
                self.divModC3d(exp1,exp2,newTemp,self.operador)
                result.tipo = exp1.tipo
            elif self.operador == Operador.POW:
                self.generator.addExpression(target=newTemp, left=f"pow({exp1.valor},{exp2.valor})", operator="",
                                                 right="")
                result.tipo = exp1.tipo
            elif self.operador == Operador.POWF:
                self.generator.addExpression(target=newTemp, left=f"pow({exp1.valor},{exp2.valor})", operator="",
                                                 right="")
                result.tipo = exp1.tipo
        else:
            error="Los nodos a operar deben de ser del mismo tipo"
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                  columna=self.columna)
        return result
    def divModC3d(self,exp1,exp2,newTemp,operador):
        self.trueLabel = self.generator.newLabel()
        salida = self.generator.newLabel()
        self.generator.addIf(left=exp2.valor, rigth="0", operator="!=",
                             label=self.trueLabel)  # if (exp2!=0) goto Lv
        self.generator.addError("Math Error!")  # imprime error en c3d
        self.generator.addExpression(target=newTemp, left="0", right="", operator="")  # tnum=0
        self.generator.addGoto(salida)  # goto Lsalida
        self.generator.addLabel(self.trueLabel)  # Lv:
        if self.operador==Operador.DIV:
            self.generator.addExpression(target=newTemp, left=exp1.valor, operator="/",
                                     right=exp2.valor)  # tnum= val1/val2
            if exp1.tipo in [Tipos.INT64,Tipos.USIZE] and exp2.tipo in [Tipos.INT64,Tipos.USIZE]:
                self.generator.addExpAsign(target=newTemp,right=f"(int){newTemp}")
        else:
            self.generator.addExpression(target=newTemp,left=f"(int){exp1.valor}",right=f"(int){exp2.valor}",operator="%")
        self.generator.addLabel(salida)  # Lsalida


    def ConcatenarStrC3d(self,posInit:str):
        contador = self.generator.newTemp()
        self.generator.addExpression(target=contador, left=posInit, right="", operator="")  # Contador = posInit;
        loop = self.generator.newLabel() # Loop
        self.trueLabel = self.generator.newLabel()  # Lv
        self.falseLabel = self.generator.newLabel()  # LF

        self.generator.addLabel(loop)  # Loop:
        texp = self.generator.newTemp()  #texp
        self.generator.addGetHeap(texp, contador)  # texp = Heap[contador];
        self.generator.addIf(left=texp, rigth="-1", operator="!=", label=self.trueLabel)  # if (texp!=-1) goto Lv
        self.generator.addGoto(self.falseLabel)  # goto Lf
        self.generator.addLabel(self.trueLabel)  # Lv:
        #vHeap = self.generator.newTemp()  # tvs
        #self.generator.addGetHeap(vHeap, contador)  # tvs = Heap[contador]
        self.generator.addSetHeap("H", texp)  # Heap[H]=texp
        self.generator.addNextHeap()  # H=H+1
        self.generator.addExpression(target=contador, left=contador, right="1", operator="+")  # contador=contador+1;
        self.generator.addGoto(loop) # goto Loop
        self.generator.addLabel(self.falseLabel) #Lf:

    def powC3d(self,exp1:ValC3d,exp2:ValC3d):
        t1=self.generator.newTemp()
        t2=self.generator.newTemp()
        tcont=self.generator.newTemp()
        taux=self.generator.newTemp()
        taux2= self.generator.newTemp()
        loop=self.generator.newLabel()
        L0=self.generator.newLabel()
        L1=self.generator.newLabel()
        Lsalida=self.generator.newLabel()
        self.generator.addExpAsign(target=t1,right=exp1.valor)# t1=v1
        self.generator.addExpAsign(target=t2, right=exp2.valor)# t2=v2
        self.generator.addExpAsign(target=tcont,right="1")# tcont=04
        self.generator.addExpAsign(target=taux, right=t2)  # taux=t2
        self.generator.addExpAsign(target=taux2,right=t1) # taux2=t1
        self.generator.addIf(left=t2,rigth="0",operator="==",label=L0)# if(t2==0) goto L0
        self.generator.addIf(left=t2,rigth="0",operator=">",label=loop)# if(t2>0) goto loop
        self.generator.addExpression(target=t2,left=t2,right="-1",operator="*")# t2=t2*-1

        self.generator.addLabel(loop)# Loop:
        self.generator.addIf(left=tcont,rigth=t2,operator=">=",label=L1)#  if(tcont => t2) goto L1
        if exp1.tipo in [Tipos.INT64,Tipos.USIZE]:
            self.generator.addExpression(target=t1,left=f"(int){t1}",right=f"(int){taux2}",operator="*")#  t1=t1*t1
        else:
            self.generator.addExpression(target=t1, left=t1, right=taux2, operator="*")
        self.generator.addExpression(target=tcont,left=tcont,right="1",operator="+")#  tcont=tcont+1
        self.generator.addGoto(loop)#  goto Loop

        self.generator.addLabel(L0)# L0:
        self.generator.addExpAsign(target=t1,right="1")# t1=1;
        self.generator.addGoto(Lsalida)# goto Lsalida
        self.generator.addLabel(L1)# L1:
        self.generator.addIf(left=taux,rigth="0",operator=">",label=Lsalida)# if(taux>0) goto Lsalida
        self.generator.addExpression(target=t1,left="1",right=t1,operator="/")# t1=1/t1;
        self.generator.addLabel(Lsalida)# Lsalida:

        return t1 #retorno de la variable con el resultado




