from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Enviroment import Enviroment
from models.Abstract.Expresion import Expresion
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d
class If_ternario(Expresion):
    def __init__(self,exp:Expresion,bloque1:[],exp1b:Expresion,bloque2:[],exp2b:Expresion,line:int,column:int):
        super().__init__()
        self.value=None
        self.tipo=None
        self.exp=exp
        self.bloque1=bloque1
        self.bloque2=bloque2
        self.exp1b=exp1b
        self.exp2b=exp2b
        self.line=line
        self.column=column
        self.instancia=0
        self.tmpR = ""
    def getTipo(self, driver, ts):
        self.resetInst()
        if self.tipo==None and self.value==None:
            self.getValor(driver,ts)
            if self.value==None:
                self.tipo==Tipos.ERROR
        else:
            self.instancia+=1

        return self.tipo

    def getValor(self, driver, ts):
        self.instancia+=1
        if self.tipo == None and self.value == None:
            newts=Enviroment(ts,"If ternario");
            t_exp = self.exp.getTipo(driver, ts)
            v_exp=self.exp.getValor(driver,ts);
            if(v_exp is not None):
                if t_exp == Tipos.BOOLEAN:
                    if v_exp==True:
                        for inst in self.bloque1:
                            inst.ejecutar(driver,newts)
                        expR=self.exp1b
                        self.tipo = expR.getTipo(driver, newts)
                        self.value=expR.getValor(driver,newts)
                    else:
                        for inst in self.bloque2:
                            inst.ejecutar(driver, newts)
                        expR = self.exp2b
                        self.tipo = expR.getTipo(driver, newts) #los ifs anidados son expresiones
                        self.value = expR.getValor(driver, newts)
                else:
                    print("la expresion debe de dar un resultado booleano")
                    error = "la expresion debe de dar un resultado booleano"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
            else:
                print("La expresion en el if causa error")
                error = "La expresion en el if causa error"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        return self.value


    def resetInst(self):
        if self.instancia>1:
            self.instancia=0
            self.value=None
            self.tipo=None
    def ejecutar(self, driver, ts):
        """En la mayoria de expresiones no realiza nada aqui"""
        pass
    def generarC3d(self,ts,ptr:int,lsalida="",aux=0):
        self.generator.addComment("If ternario")

        if self.tmpR == "": #todos los resultados apuntaran al mismo tmpR de este if
            self.tmpR = self.generator.newTemp()

        newts=Enviroment(ts,"If ternario")
        newts.generator = self.generator
        trueL = self.generator.newLabel()
        falseL = self.generator.newLabel()
        tmp_r=self.generator.newTemp()
        falseLr=self.generator.newLabel()
        trueLr=self.generator.newLabel()
        if lsalida=="":
            lsalida=self.generator.newLabel()
            self.generator.addComment("IF")
        else:
            self.generator.addComment("ELSE IF ")
        result = ValC3d(valor=self.tmpR, isTemp=True, tipo=Tipos.ERROR)
        self.exp.generator = self.generator
        self.exp.falseLabel=falseL
        self.exp.trueLabel=trueL
        self.generator.addComment("Condicion del if")
        exp:ValC3d=self.exp.generarC3d(ts,ptr)
        self.generator.addComment("Fin condicion del If")
        if exp.tipo==Tipos.BOOLEAN:
            self.generator.addLabel(trueL)
            self.generator.addNextStack(index=str(ts.size))
            for ins in self.bloque1:
                ins.generator=self.generator
                ins.generarC3d(newts,ptr)
            self.exp1b.generator = self.generator
            e_aux=self.exp1b.generarC3d(newts,ptr)
            # ESTO SOLO SE HACE UNA VEZ, YA QUE EL IF TERNARIO DEBE DE CONTENER SOLO VALORES DEL MISMO TIPO
            result.tipo=e_aux.tipo
            result.tipo_aux=e_aux.tipo_aux
            result.trueLabel=trueLr
            result.falseLabel=falseLr
            result.prof_array = e_aux.prof_array

            self.generator.addExpAsign(target=self.tmpR,right=e_aux.valor)
            self.generator.addBackStack(index=str(ts.size))
            self.generator.addGoto(lsalida)
            self.generator.addLabel(falseL)

            if not isinstance(self.exp2b, If_ternario):
                self.generator.addComment("ELSE")
                self.generator.addNextStack(index=str(ts.size))  # para que la pila se mueva el nuevo enviroment
                # se debe de sumar el tamaño del anterior
                newts = Enviroment(ts, "If")
                newts.generator = self.generator
                for ins in self.bloque2:
                    ins.generator = self.generator
                    ins.generarC3d(newts, ptr)
                    if self.exp2b != None:
                        self.exp2b.generator = self.generator
                        e_aux = self.exp2b.generarC3d(newts, ptr)
                        self.generator.addExpAsign(target=self.tmpR, right=e_aux.valor)
                self.generator.addBackStack(index=str(ts.size))
            else:
                self.exp2b.generator = self.generator
                self.exp2b.tmpR = self.tmpR
                self.exp2b.generarC3d(ts, ptr, lsalida, 1)

        else:
            error="La expresion del if debe de ser una expresion booleana"
            print(error)
        if aux == 0:
            self.generator.addLabel(lsalida)
        self.generator.addComment("End If ternario")
        return result