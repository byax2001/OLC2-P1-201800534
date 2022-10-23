from models.Expresion.Operacion.OperacionLog import OperacionLog, OperadorLog, getOperador
from models.TablaSymbols.Tipos import Tipos,definirTipo
from models.TablaSymbols.ValC3d import ValC3d
from BaseDatos.B_datos import B_datos
class Logicas(OperacionLog): #de esta forma se esta indicando que aritmeticas hereda de Operacion
    #var Operacion: exp1: Expresion, operador, exp2: Expresion, linea, columna, expU
    def getTipo(self, driver, ts):
        self.resetInst()
        if self.value==None and self.tipo==None:
            self.getValor(driver,ts)
            if self.value==None:
                self.tipo=Tipos.ERROR
        else:
            self.instancia+=1
        return self.tipo

    # get valor con condicionales
    def getValor(self, driver, ts):
        self.instancia+=1;

        if self.value==None and self.tipo==None:
            t_nodoIzq = self.exp1.getTipo(driver, ts)
            t_nodoDer = self.exp2.getTipo(driver, ts) if not self.expU else None
            if t_nodoIzq==t_nodoDer:
                if t_nodoIzq==Tipos.BOOLEAN:
                    if self.operador==OperadorLog.AND:
                        valor1 = self.exp1.getValor(driver, ts)
                        if valor1 == False:
                            self.value = False
                            valor2 = self.exp2.getValor(driver, ts)
                        else:
                            valor2 = self.exp2.getValor(driver, ts)
                            self.value = valor1 and valor2
                        self.tipo = Tipos.BOOLEAN
                    elif self.operador==OperadorLog.OR:
                        valor1=self.exp1.getValor(driver,ts)
                        if valor1==True:
                            self.value=True
                            valor2=self.exp2.getValor(driver,ts)
                        else:
                            valor2 = self.exp2.getValor(driver, ts)
                            self.value= valor1 or valor2
                        self.tipo = Tipos.BOOLEAN
                else:
                    print("Ambos datos a comparar deben de ser valores booleanos")
                    error = "Ambos datos a comparar deben de ser valores booleanos "
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                      columna=self.columna)
            elif t_nodoIzq==Tipos.BOOLEAN and t_nodoDer==None:
                if self.operador == OperadorLog.NOT:
                    self.value = not (self.exp1.getValor(driver, ts))
                    self.tipo = Tipos.BOOLEAN
            else:
                print("Se intenta hacer una operacion Logica con uno o dos nodos no Booleanos")
                error = "Se intenta hacer una operacion Logica con uno o dos nodos no Booleanos "
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                                  columna=self.columna)
        return self.value
    def ejecutar(self, driver, ts):
        """En la mayoria de expresiones no realiza nada"""
        pass

    def resetInst(self):
        if self.instancia>1:
            self.instancia=0
            self.value=None
            self.tipo=None
    def generarC3d(self,ts,ptr:int):
        self.generator.addComment("Logicas")
        if (self.trueLabel == ""):
            self.trueLabel = self.generator.newLabel()  # Ln: (true)

        if (self.falseLabel == ""):
            self.falseLabel = self.generator.newLabel()  # Ln+1: (false)   pag  404

        self.exp1.generator=self.generator
        if self.exp2 != None:
            self.exp2.generator=self.generator
        val:ValC3d = ValC3d(valor="",isTemp=False,tipo=Tipos.BOOLEAN,tipo_aux=Tipos.BOOLEAN)
        if self.operador==OperadorLog.AND:
            self.generator.addLabel("Logica: And")
            # B -> B1 && B2  |  B1.true = B.nuevaetiqueta()
            #                |  B1.false = B.false
            #                |  B2.true = B.true
            #                |  B2.false = B.false
            #                |  B.codigo = B1.codigo +  etiqueta(B1.true) + B2.codigo
            self.exp1.trueLabel=self.generator.newLabel()
            self.exp1.falseLabel=self.falseLabel
            self.exp2.trueLabel=self.trueLabel
            self.exp2.falseLabel=self.falseLabel
            izq_r:ValC3d=self.exp1.generarC3d(ts,ptr)
            self.generator.addLabel(izq_r.trueLabel)
            self.exp2.generarC3d(ts,ptr)
            val.trueLabel=self.trueLabel
            val.falseLabel=self.falseLabel
        elif self.operador==OperadorLog.OR:
            self.generator.addLabel("Logica: Or")
            # B -> B1 || B2  |  B1.true = B.true
            #                |  B1.false = nuevaetiqueta()
            #                |  B2.true = B.true
            #                |  B2.false = B.false
            #                |  B.codigo = B1.codigo +  etiqueta(B1.false) + B2.codigo
            self.exp1.trueLabel = self.trueLabel
            self.exp1.falseLabel = self.generator.newLabel()
            self.exp2.trueLabel = self.trueLabel
            self.exp2.falseLabel = self.falseLabel
            izq_r: ValC3d = self.exp1.generarC3d(ts, ptr)
            self.generator.addLabel(izq_r.falseLabel)
            self.exp2.generarC3d(ts, ptr)
            val.trueLabel = self.trueLabel
            val.falseLabel = self.falseLabel
        elif self.operador==OperadorLog.NOT:
            self.generator.addLabel("Logica: Not")
            self.exp1.trueLabel=self.falseLabel
            self.exp1.falseLabel=self.trueLabel
            self.exp1.generarC3d(ts,ptr)
            val.trueLabel = self.trueLabel
            val.falseLabel = self.falseLabel
        return val
