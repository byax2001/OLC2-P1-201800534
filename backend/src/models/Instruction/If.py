from models.Abstract.Instruction import Instruccion
from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.Tipos import Tipos
from models.Instruction.Break import Break
from models.Instruction.Continue import Continue
from models.Instruction.Return import Return
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d
class If(Instruccion):
    def __init__(self,exp:Expresion,bloque1:[Instruccion],bloque2:[Instruccion],line:int,column:int):
        super().__init__()
        self.exp=exp
        self.bloque1=bloque1
        self.bloque2=bloque2
        self.line=line
        self.column=column

    def ejecutar(self, driver, ts: Enviroment):
        t_exp = self.exp.getTipo(driver, ts);
        v_exp=self.exp.getValor(driver,ts); # con el ts anterior
        new_ts=Enviroment(ts,"IF"); #ejecutar resto de instrucciones con el nuevo ts
        if(v_exp is not None):
            if t_exp ==Tipos.BOOLEAN:
                if v_exp==True:
                    for element in self.bloque1:
                        if isinstance(element,Break) or isinstance(element,Continue) or isinstance(element,Return):
                            return element
                        rInst=element.ejecutar(driver,new_ts)
                        if isinstance(rInst,Break) or isinstance(rInst,Continue) or isinstance(rInst,Return):
                            return rInst
                else:
                    for element in self.bloque2:
                        if isinstance(element, Break) or isinstance(element, Continue) or isinstance(element, Return):
                            return element
                        rInst = element.ejecutar(driver,new_ts)
                        if isinstance(rInst, Break) or isinstance(rInst, Continue) or isinstance(rInst, Return):
                            return rInst
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

    def generarC3d(self,ts:Enviroment,ptr,lsalida="",aux=0):
        self.generator.addComment("If instruction")
        tn_rif=self.generator.newTemp()
        result_if=ValC3d(valor=tn_rif,isTemp=True,tipo=Tipos.ERROR,tipo_aux=Tipos.ERROR)
        newts=Enviroment(ts,"If")
        newts.generator=self.generator
        truelabel=self.generator.newLabel()
        falselabel=self.generator.newLabel()
        if lsalida=="":
            lsalida=self.generator.newLabel()
        self.exp.trueLabel=truelabel
        self.exp.falseLabel=falselabel
        self.exp.generator=self.generator
        r_exp:ValC3d=self.exp.generarC3d(ts,ptr)

        if r_exp.tipo==Tipos.BOOLEAN:
            self.generator.addLabel(truelabel)
            self.generator.addNextStack(index=str(ts.size))
            for ins in self.bloque1:
                ins.generator=self.generator
                result=ins.generarC3d(newts,{"tmpR":ptr,"envAnt":ts.size})
                if result!=None:
                    result_if.tipo=result.tipo
                    result_if.tipo_aux=result.tipo
                    result_if.trueLabel=result.trueLabel
                    result_if.falseLabel=result.falseLabel
            self.generator.addBackStack(index=str(ts.size))
            self.generator.addGoto(lsalida)
            self.generator.addLabel(falselabel)
            if len(self.bloque2)!=0:
                if not isinstance(self.bloque2[0],If):
                    self.generator.addNextStack(index=str(ts.size)) #para que la pila se mueva el nuevo enviroment
                                                                    # se debe de sumar el tamaño del anterior
                    newts = Enviroment(ts, "If")
            for ins in self.bloque2:
                if isinstance(ins,If):
                    ins.generator = self.generator
                    ins.generarC3d(newts, ptr,lsalida,1)
                else:
                    ins.generator = self.generator
                                                 #tmpR: label exit luego de un return o break
                                                 #envAnt: para retroceder la pila al enviroment anterior
                    result=ins.generarC3d(newts, {"tmpR":ptr,"envAnt":ts.size})
                    if result != None:
                        result_if.tipo = result.tipo
                        result_if.tipo_aux = result.tipo
                        result_if.trueLabel = result.trueLabel
                        result_if.falseLabel = result.falseLabel
                    self.generator.addBackStack(index=str(ts.size))
        else:
            error="La expresion debe de ser de tipo booleano"
            print(error)
        if aux==0:
            self.generator.addLabel(lsalida)

            self.generator.addComment("End If")
        return result_if

