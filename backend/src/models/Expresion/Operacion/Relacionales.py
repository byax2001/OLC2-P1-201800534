from models.Expresion.Operacion.OperacionRel import OperacionRel, OperadorRel, strOperador
from models.TablaSymbols.Tipos import Tipos,definirTipo
from models.TablaSymbols.ValC3d import ValC3d
from BaseDatos.B_datos import B_datos
class Relacionales(OperacionRel): #de esta forma se esta indicando que aritmeticas hereda de Operacion
    #var Operacion: exp1: Expresion, operador, exp2: Expresion, linea, columna, expU
    def getTipo(self, driver, ts):
        self.resetInst()
        if self.tipo==None and self.value==None:
            self.getValor(driver, ts)
            if self.value==None:
                self.tipo==Tipos.ERROR
        else:
            self.instancia+=1
        return self.tipo

    # get valor con condicionales
    def getValor(self, driver, ts):
        self.instancia+=1
        if self.tipo==None and self.value==None:
            t_nodoIzq = self.exp1.getTipo(driver, ts)
            v_nodoIzq = self.exp1.getValor(driver, ts)
            t_nodoDer = self.exp2.getTipo(driver, ts)
            v_nodoDer = self.exp2.getValor(driver,ts)
            if t_nodoDer==t_nodoIzq:
                self.value= self.comparar(v_nodoIzq,v_nodoDer)
                self.tipo=definirTipo(self.value)
            elif t_nodoIzq in [Tipos.INT64, Tipos.USIZE] and t_nodoDer in [Tipos.INT64, Tipos.USIZE]:
                self.value=  self.comparar(v_nodoIzq,v_nodoDer)
                self.tipo = definirTipo(self.value)
            else:
                print("Las literales a comparar no son del mismo tipo ")
                error = "Las literales a comparar no son del mismo tipo"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                  columna=self.columna)
        return self.value
    def comparar(self,valor1,valor2):
        if self.operador == OperadorRel.MAYORQUE:
            return valor1 > valor2
        elif self.operador == OperadorRel.MENORQUE:
            return valor1 < valor2
        elif self.operador == OperadorRel.MAYORIGUALQUE:
            return valor1 >= valor2
        elif self.operador == OperadorRel.MENORIGUALQUE:
            return valor1 <= valor2
        elif self.operador == OperadorRel.IGUALQUE:
            return valor1 == valor2
        elif self.operador == OperadorRel.DIFERENTEQUE:
            return valor1 != valor2

    def ejecutar(self, driver, ts):
        """En la mayoria de expresiones no realiza nada"""
        pass
    def resetInst(self):
        if self.instancia>1:
            self.instancia=0
            self.value=None
            self.tipo=None
    def generarC3d(self,ts,ptr:int):
        self.generator.addComment("Operaciones Relacionales")
        self.exp1.generator=self.generator
        self.exp2.generator=self.generator
        if self.trueLabel=="":
            self.trueLabel=self.generator.newLabel()
        if self.falseLabel=="":
            self.falseLabel=self.generator.newLabel()

        self.exp1.trueLabel=self.exp2.trueLabel=self.trueLabel
        self.exp1.falseLabel=self.exp2.falseLabel=self.falseLabel

        val1:ValC3d=self.exp1.generarC3d(ts,ptr)
        val2:ValC3d=self.exp2.generarC3d(ts,ptr)
        if val1.tipo==val2.tipo:
            valor = ValC3d(valor="", isTemp=False, tipo=Tipos.BOOLEAN, tipo_aux=Tipos.BOOLEAN)
            if val1.tipo in [Tipos.STR,Tipos.STRING]:
                self.cmpStrC3d(i_str1=val1.valor,i_str2=val2.valor)
                valor.trueLabel=self.trueLabel
                valor.falseLabel=self.falseLabel
            elif val1.tipo==Tipos.BOOLEAN:
                #para ==  seria literalmente un and:    true && true por ejemplo
                # para !=  seria literalmente un:  true &&  !true
                gotov2:str=self.generator.code.pop()
                gotov1:str=self.generator.code.pop()
                v2 = "0"
                v1 = "0"
                if self.trueLabel in gotov2:
                    v2="1"
                if self.trueLabel in gotov1:
                    v1="1"
                self.generator.addIf(left=v1, rigth=v2, operator=strOperador(self.operador),
                                     label=self.trueLabel)
                self.generator.addGoto(label=self.falseLabel)
                valor.trueLabel = self.trueLabel
                valor.falseLabel = self.falseLabel
            else:
                self.generator.addIf(left=val1.valor,rigth=val2.valor,operator=strOperador(self.operador),label=self.trueLabel)
                self.generator.addGoto(label=self.falseLabel)
                valor.trueLabel=self.trueLabel
                valor.falseLabel=self.falseLabel
            return valor
        else:
            error="Las literales a comparar no son del mismo tipo"
            print(error)

    def cmpBoolC3d(self):
        print()

    def cmpStrC3d(self,i_str1,i_str2):
        t1= self.generator.newTemp()
        t2= self.generator.newTemp()
        t3=self.generator.newTemp()
        t4=self.generator.newTemp()
        loop=self.generator.newLabel()
        lim1=self.generator.newLabel()
        self.generator.addExpAsign(target=t1,right=i_str1) #    t1 = init1
        self.generator.addExpAsign(target=t2, right=i_str2)#    t2 = init2
        self.generator.addLabel(label=loop)                #    loop:
        self.generator.addGetHeap(target=t3,index=t1)      #    t3 = Stack[t1]
        self.generator.addGetHeap(target=t4, index=t2)     #    t4 = Stack[t2]
        self.generator.addExpression(target=t1,left=t1,right="1",operator="+")# t1 = t1 + 1
        self.generator.addExpression(target=t2, left=t2, right="1", operator="+")# t2 = t2 + 1
        self.generator.addIf(left=t3,rigth="-1",operator="==",label=lim1)       # if (t3 == -1) goto Lim1

        # --------- si la cadena 2 llego a su limite pero no la 1 entonces no son iguales
        if self.operador=="==":
            self.generator.addIf(left=t4, rigth="-1", operator="==", label=self.falseLabel) #if (t4 == -1) goto LF
            self.generator.addIf(left=t3, rigth=t4, operator="==", label=loop)  # if (t3 == t4) goto Loop
            self.generator.addGoto(self.falseLabel)  # goto LF
            self.generator.addLabel(lim1)  # Lim1:
            self.generator.addIf(left=t4, rigth="-1", operator="==", label=self.trueLabel)  # if (t4==-1) goto LV
            self.generator.addGoto(self.falseLabel)  # goto LF
        else:
            #si las cadenas no son iguales, entonces es verdadero el !=
            self.generator.addIf(left=t4, rigth="-1", operator="==", label=self.trueLabel)  # if (t4 == -1) goto LV
            self.generator.addIf(left=t3, rigth=t4, operator="==", label=loop)  # if (t3 == t4) goto Loop
            self.generator.addGoto(self.trueLabel)  # goto LV   Las cadenas no fueron iguales en algun punto: cumple con !=
            self.generator.addLabel(lim1)  # Lim1:
            # if (t4==-1) goto LF ambas cadenas son iguales y terminan donde mismo, entonces no cumplen con el !=
            self.generator.addIf(left=t4, rigth="-1", operator="==", label=self.falseLabel)   # goto LF
            # ambas cadenas poseen elementos similares pero no terminan al mismo tiempo, por lo que no son iguales
            # lo que cumple con !=
            self.generator.addGoto(self.trueLabel)  # goto LV



