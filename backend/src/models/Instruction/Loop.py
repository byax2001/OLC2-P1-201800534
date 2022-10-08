from models.Abstract.Instruction import Instruccion
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.Tipos import Tipos
from models.Instruction.Break import Break
from models.Instruction.Continue import Continue
from models.Instruction.Return import Return
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d
class Loop(Instruccion):
    def __init__(self,bloque:[Instruccion],line:int,column:int):
        super().__init__()
        self.tipo=None
        self.value=None
        self.bloque=bloque
        self.line=line
        self.column=column
        self.instancia=0
    def ejecutar(self, driver, ts: Enviroment):
        while True:
            new_ts= Enviroment(ts,"Loop");
            for instruccion in self.bloque:
                if isinstance(instruccion, Break):
                    return
                elif isinstance(instruccion, Continue):
                    break;
                elif isinstance(instruccion, Return):
                    print("Error, existe return afuera de una funcion")
                    error = "Error, existe return afuera de una funcion"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
                    return
                rInst = instruccion.ejecutar(driver,new_ts)
                if isinstance(rInst, Break):
                    return
                elif isinstance(rInst, Continue):
                    break;
                elif isinstance(rInst, Return):
                    print("Error, existe return afuera de una funcion")
                    error = "Error, existe return afuera de una funcion"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
                    return
    #esto solo se usara cuando se use como expresion
    def getValor(self, driver, ts):
        self.instancia+=1
        self.resetInst()
        if self.value==None:
            while True:
                for instruccion in self.bloque:
                    if isinstance(instruccion, Break):
                        self.value=instruccion.getValor(driver,ts)
                        self.tipo=instruccion.getTipo(driver,ts)
                        return self.value
                    elif isinstance(instruccion, Continue):
                        break
                    elif isinstance(instruccion, Return):
                        print("Error, existe return afuera de una funcion")
                        error = "Error, existe return afuera de una funcion"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                          columna=self.column)
                        return
                    rInst = instruccion.ejecutar(driver, ts)
                    if isinstance(rInst, Break):
                        self.value = rInst.getValor(driver, ts)
                        self.tipo = rInst.getTipo(driver, ts)
                        return self.value
                    elif isinstance(rInst, Continue):
                        break
                    elif isinstance(rInst, Return):
                        print("Error, existe return afuera de una funcion")
                        error = "Error, existe return afuera de una funcion"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                          columna=self.column)
                        return
        else:
            return self.value
    def getTipo(self, driver, ts):
        if self.tipo== None:
            self.getValor(driver,ts)
            if self.tipo==None: #si despues de eso sigue siendo None, significa que ocurrio un error
                self.tipo=Tipos.ERROR
            return self.tipo
        else:
            return self.tipo
    def resetInst(self):
        if self.instancia>2:
            self.instancia=0
            self.value=None
            self.tipo=None
    def generarC3d(self,ts,ptr:int):
        self.generator.addComment("Loop Instruction")
        tn_rloop=self.generator.newTemp()
        rloop=ValC3d(valor=tn_rloop,isTemp=True,tipo=Tipos.ERROR,tipo_aux=Tipos.ERROR)
        # Loop:
        # 	<Instrucciones>
        # 	goto Loop
        # Salida:
        loop=self.generator.newLabel()
        lexit=self.generator.newLabel()
        self.generator.addLabel(loop)
        init_code=len(self.generator.code)
        for ins in self.bloque:
            ins.generator=self.generator
            result=ins.generarC3d(ts,ptr=tn_rloop)
            if result!=None:
                rloop.tipo = result.tipo
                rloop.tipo_aux = result.tipo
                rloop.trueLabel = result.trueLabel
                rloop.falseLabel = result.falseLabel
        f_code = len(self.generator.code)
        code=""
        for x in range(init_code,f_code):
            if x!=f_code-1:
                code+=self.generator.code[x]+"\n"
            else:
                code += self.generator.code[x]
        for x in reversed(range(init_code,f_code)):
            self.generator.code.pop(x)
        code=code.replace("break_i",f"goto {lexit};")
        self.generator.addCode(code)
        self.generator.addGoto(loop)
        self.generator.addLabel(lexit)
        return rloop