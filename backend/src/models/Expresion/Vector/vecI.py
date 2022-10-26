from models.TablaSymbols.Tipos import Tipos
from models.Abstract.Expresion import Expresion
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d

#dec vector vacio
#  vectorI == vec!
class vecI(Expresion):
    def __init__(self,cExp:[Expresion],exp:Expresion,multiplicador:Expresion,line:int,column:int):
        super().__init__()
        self.value=None
        self.tipo=None
        self.cExp=cExp
        self.line=line
        self.column=column
        self.exp=exp
        self.multi=multiplicador
        self.instancia=0
        self.profundidad=0
    def getValor(self, driver, ts):
        vector=[]
        self.instancia+=1
        if self.value == None and self.tipo == None:
            if self.exp==None:
                x=0
                tipoaux=Tipos.ERROR
                for exp in self.cExp:
                    if x==0:
                        tipoaux=exp.getTipo(driver,ts)
                        valor=exp.getValor(driver,ts)
                        vector.append({"valor":valor,"tipo":tipoaux})
                        x+=1
                    else:
                        tipo2=exp.getTipo(driver,ts)
                        valor2=exp.getValor(driver,ts)
                        if tipo2!=tipoaux:
                            self.tipo==Tipos.ERROR
                            self.value=None
                            print(f"Error uno de los elementos del vector no es del mismo tipo que el resto {self.line}")
                            error = "Error uno de los elementos del vector no es del mismo tipo que el resto"
                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                              columna=self.column)
                            return
                        vector.append({"valor": valor2, "tipo": tipo2})
                self.value=vector
                self.tipo=tipoaux
            else:
                if self.multi.getTipo(driver,ts)==Tipos.INT64:
                    valor=self.exp.getValor(driver,ts)
                    tipo=self.exp.getTipo(driver,ts)
                    if tipo!=Tipos.ERROR:
                        multi = self.multi.getValor(driver, ts)
                        if self.multi.getTipo(driver,ts)==Tipos.INT64:
                            x=0;
                            while x!=multi:
                                vector.append({"valor":valor,"tipo":tipo})
                                x+=1
                            self.value=vector
                            self.tipo=tipo
                        else:
                            print(f"el multiplicador para el vector no es un entero {self.line}")
                            error = "el multiplicador para el vector no es un entero"
                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                              columna=self.column)
                    else:
                        print("La expresion a multiplicar en una array da error"+str(self.line))
                        error = "La expresion a multiplicar en una array da error"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                          columna=self.column)
                else:
                    print("Error el multiplicador no es integer")
                    error = "Error el multiplicador no es integer"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
        return self.value

    def getTipo(self, driver, ts):
        self.resetInst()
        if self.value==None and self.tipo==None:
            self.getValor(driver,ts)
            if self.value == None:  # si despues de eso sigue siendo None ocurrio un error
                self.tipo = Tipos.ERROR
        else:
            self.instancia+=1
        return self.tipo
    def resetInst(self):
        if self.instancia>1:
            self.instancia=0
            self.value=None
            self.tipo=None
    def generarC3d(self,ts,ptr):
        self.generator.addComment("Exp Vec!")
        tmpR = self.generator.newTemp()
        result = ValC3d(valor=tmpR, isTemp=True, tipo=Tipos.ERROR, tipo_aux=Tipos.ARREGLO)
        lexp = []
        if self.exp == None:  # si es un arreglo normal y no un [exp;multiplicador]
            x = 0
            for exp in self.cExp:
                exp.generator = self.generator
                rexp: ValC3d = exp.generarC3d(ts, ptr)
                if x == 0:
                    result.tipo = rexp.tipo
                    x += 1
                if rexp.tipo == rexp.tipo_aux == Tipos.BOOLEAN:
                    self.generator.addComment("Exp Bool")
                    trbool = self.generator.newTemp()
                    exit = self.generator.newLabel()
                    self.generator.addLabel(rexp.trueLabel)
                    self.generator.addExpAsign(target=trbool, right="1")
                    self.generator.addGoto(exit)
                    self.generator.addLabel(rexp.falseLabel)
                    self.generator.addExpAsign(target=trbool, right="0")
                    self.generator.addLabel(exit)
                    lexp.append(trbool)
                else:
                    lexp.append(rexp.valor)
            result.tipo_aux = Tipos.VECTOR
            self.generator.addExpAsign(target=tmpR, right="H")
            self.generator.addComment("Tamanio Vec!")
            self.generator.addSetHeap(index="H", value=str(len(lexp)))  # tamaño del arreglo
            self.generator.addNextHeap()
            self.generator.addComment("---------------")
            self.generator.addComment("Capacity del vec")
            self.generator.addSetHeap(index="H", value=str(len(lexp)))  # capacity del vector
            self.generator.addNextHeap()
            self.generator.addComment("---------------")
            for exp in lexp:
                self.generator.addSetHeap(index="H", value=exp)
                self.generator.addNextHeap()
        else:
            # tcont= 0
            # taux= valormul
            # Heap[H]=taux  //tamaño del arreglo como primer elemento
            # H=H+1
            # tvalor=valor
            # Loop:
            # if(tcont>=taux) goto Lsalida
            # Heap[H]=tvalor
            # H=H+1
            # tcont=tcont+1;
            # goto Loop
            # Lsalida
            self.generator.addExpAsign(target=tmpR, right="H")
            tcont = self.generator.newTemp()
            taux = self.generator.newTemp()
            loop = self.generator.newLabel()
            lsalida = self.generator.newLabel()
            self.generator.addExpAsign(target=tcont, right="0")  # tcont= 0
            self.multi.generator = self.generator
            rmul: ValC3d = self.multi.generarC3d(ts, ptr)
            if rmul.tipo in [Tipos.INT64, Tipos.USIZE]:
                self.generator.addExpAsign(target=taux, right=rmul.valor)  # taux= valormul
            else:
                error = "El multiplicador debe de ser un dato entero"
                print(error)
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
                return result
            self.generator.addComment("Tamanio Vec!")
            self.generator.addSetHeap(index="H", value=taux) # array[0] tamaño del vector
            self.generator.addNextHeap()
            self.generator.addComment("---------------")
            self.generator.addComment("Capacity del vec")
            self.generator.addSetHeap(index="H", value=taux)  # capacity del vector
            self.generator.addNextHeap()
            self.generator.addComment("---------------")
            # tvalor=valor
            self.exp.generator = self.generator
            rval = self.exp.generarC3d(ts, ptr)
            result.tipo = rval.tipo
            result.tipo_aux = rval.tipo_aux
            tvalor = self.generator.newTemp()
            if rval.tipo == rval.tipo_aux == Tipos.BOOLEAN:
                tvalor = self.generator.newTemp()
                exit = self.generator.newLabel()
                self.generator.addLabel(result.trueLabel)
                self.generator.addExpAsign(target=tvalor, right="1")
                self.generator.addGoto(exit)
                self.generator.addLabel(result.falseLabel)
                self.generator.addExpAsign(target=tvalor, right="0")
                self.generator.addLabel(exit)
                self.generator.addNextHeap()
            else:
                self.generator.addExpAsign(target=tvalor, right=rval.valor)

            self.generator.addLabel(loop)  # Loop:
            self.generator.addIf(left=tcont, rigth=taux, operator=">=", label=lsalida)  ##if(tcont>=taux) goto Lsalida
            self.generator.addSetHeap(index="H", value=tvalor)  # #Heap[H]=tvalor
            self.generator.addNextHeap()  # #H=H+1
            self.generator.addExpression(target=tcont, left=tcont, right="1", operator="+")  # tcont=tcont+1;
            self.generator.addGoto(loop)  # goto Loop
            self.generator.addLabel(lsalida)  # Lsalida:

        result.prof_array = self.profundidad
        return result

