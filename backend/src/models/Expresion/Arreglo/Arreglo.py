from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.ValC3d import ValC3d
class Arreglo(Expresion):
    def __init__(self,cExp:Expresion,exp:Expresion,multi:Expresion,line:int,column:int):
        super().__init__()
        self.value=None
        self.tipo=None
        self.cExp=cExp # ["hola","hola","hola"]
        self.exp=exp   #[ "hola" ; 3 ]
        self.multi=multi
        self.line=line
        self.column=column
        self.instancia=0
        self.profundidad=0

    def getValor(self, driver, ts:Enviroment):
        self.instancia += 1
        vector=[]
        if self.tipo==None and self.value==None:
            x = 0
            tipoaux = Tipos.ERROR
            if self.exp==None: #expresion a multiplicar

                for exp in self.cExp:
                    if x == 0:
                        tipoaux = exp.getTipo(driver, ts)
                        valor = exp.getValor(driver, ts)
                        vector.append({"valor": valor, "tipo": tipoaux})
                        x += 1
                    else:
                        tipo2 = exp.getTipo(driver, ts)
                        valor2 = exp.getValor(driver, ts)
                        if tipo2 != tipoaux:
                            self.tipo == Tipos.ERROR
                            self.value = None
                            print(f"Error uno de los elementos del arreglo no es del mismo tipo al resto linea: {self.line}")
                            error = f"Error uno de los elementos del arreglo no es del mismo tipo al resto"
                            B_datos().appendE(descripcion=error,ambito=ts.env,linea=self.line,columna=self.column)
                            return
                        vector.append({"valor": valor2, "tipo": tipo2})
                self.value = vector
                self.tipo = tipoaux
            else:
                v_exp=self.exp.getValor(driver,ts)
                t_exp=self.exp.getTipo(driver,ts)
                v_mult=self.multi.getValor(driver,ts)
                t_mult=self.multi.getTipo(driver,ts)
                if t_mult==Tipos.INT64 and t_exp!=Tipos.ERROR:
                    for x in range(v_mult):
                        vector.append({"valor":v_exp,"tipo":t_exp})
                    self.tipo=t_exp
                    self.value = vector
                else:
                    self.tipo=Tipos.ERROR
                    print(f"Error el numero de veces a multiplicar la expresion no es entero o la expresion causa error {self.line}")
                    error = f"Error el numero de veces a multiplicar la expresion no es entero o la expresion causa error"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line, columna=self.column)
        return self.value

    def getTipo(self, driver, ts):
        self.resetInst()
        if self.tipo==None and self.value==None:
            self.getValor(driver,ts)
            if self.tipo==None:
                self.tipo==Tipos.ERROR
        else:
            self.instancia+=1
        return self.tipo
    def ejecutar(self,driver,ts):
        pass
    def resetInst(self):
        if self.instancia>1:
            self.instancia=0
            self.value=None
            self.tipo=None

       #REVISAR: QUE EL TIPO DE VARIABLE  DEL ARREGLO SEA IGUAL A TODOS LOS ELEMENTOS QUE CONTIENE
    def generarC3d(self,ts,ptr):
        self.generator.addComment("Exp Arreglo")
        tmpR=self.generator.newTemp()
        result=ValC3d(valor=tmpR,isTemp=True,tipo=Tipos.ERROR,tipo_aux=Tipos.ARREGLO)
        lexp=[]
        if self.exp==None:#si es un arreglo normal y no un [exp;multiplicador]
            x=0
            for exp in self.cExp:
                if x==0:
                    result.tipo=exp.tipo
                    x+=1
                exp.generator=self.generator
                rexp:ValC3d=exp.generarC3d(ts,ptr)
                if rexp.tipo==rexp.tipo_aux==Tipos.BOOLEAN:
                    self.generator.addComment("Exp Bool")
                    trbool=self.generator.newTemp()
                    exit=self.generator.newLabel()
                    self.generator.addLabel(rexp.trueLabel)
                    self.generator.addExpAsign(target=trbool,right="1")
                    self.generator.addGoto(exit)
                    self.generator.addLabel(rexp.falseLabel)
                    self.generator.addExpAsign(target=trbool,right="0")
                    self.generator.addLabel(exit)
                    lexp.append(trbool)
                else:
                    lexp.append(rexp.valor)
            self.generator.addExpAsign(target=tmpR,right="H")
            self.generator.addComment("Tamanio Arreglo")
            self.generator.addSetHeap(index="H",value=str(len(lexp))) #tamaño del arreglo
            self.generator.addComment("---------------")
            self.generator.addNextHeap()
            for exp in lexp:
                self.generator.addSetHeap(index="H",value=exp)
                self.generator.addNextHeap()
        else:
            # tcont= 0
            # taux= valormul
            # Heap[H]=taux  //tamaño del arreglo como primer elemento
            # tvalor=valor
            # Loop:
            # if(tcont>=taux) goto Lsalida
            # Heap[H]=tvalor
            # H=H+1
            # tcont=tcont+1;
            # goto Loop
            # Lsalida
            self.generator.addExpAsign(target=tmpR,right="H")
            tcont=self.generator.newTemp()
            taux=self.generator.newTemp()
            loop=self.generator.newLabel()
            lsalida=self.generator.newLabel()
            self.generator.addExpAsign(target=tcont,right="0") #tcont= 0
            self.multi.generator=self.generator
            rmul:ValC3d=self.multi.generarC3d(ts,ptr)
            if rmul.tipo in [Tipos.INT64,Tipos.USIZE]:
                self.generator.addExpAsign(target=taux,right=rmul.valor)# taux= valormul
            else:
                error="El multiplicador debe de ser un dato entero"
                print(error)
                return result
            #array[0] tamaño del array
            self.generator.addSetHeap(index="H",value=taux)
            # tvalor=valor
            self.exp.generator=self.generator
            rval=self.exp.generarC3d(ts,ptr)
            result.tipo=rval.tipo
            result.tipo_aux=rval.tipo_aux
            tvalor=self.generator.newTemp()
            if rval.tipo==rval.tipo_aux==Tipos.BOOLEAN:
                tvalor= self.generator.newTemp()
                exit = self.generator.newLabel()
                self.generator.addLabel(result.trueLabel)
                self.generator.addExpAsign(target=tvalor, right="1")
                self.generator.addGoto(exit)
                self.generator.addLabel(result.falseLabel)
                self.generator.addExpAsign(target=tvalor, right="0")
                self.generator.addLabel(exit)
                self.generator.addNextHeap()
            else:
                self.generator.addExpAsign(target=tvalor,right=rval.valor)

            self.generator.addLabel(loop) #Loop:
            self.generator.addIf(left=tcont,rigth=taux,operator=">=",label=lsalida) ##if(tcont>=taux) goto Lsalida
            self.generator.addSetHeap(index="H",value=tvalor) #   #Heap[H]=tvalor
            self.generator.addNextHeap()#    #H=H+1
            self.generator.addExpression(target=tcont,left=tcont,right="1",operator="+")#tcont=tcont+1;
            self.generator.addGoto(loop) #goto Loop
            self.generator.newLabel(lsalida)#Lsalida:
        result.prof_array=self.profundidad
        return result

