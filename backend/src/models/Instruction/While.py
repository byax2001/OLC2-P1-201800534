from models.Abstract.Instruction import Instruccion
from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models import Driver
from models.Instruction.Break import Break
from models.Instruction.Return import Return
from models.Instruction.Continue import Continue
from models.TablaSymbols.Tipos import Tipos
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d

class While(Instruccion):
    def __init__(self,exp:Expresion,bloque:[Instruccion],line:int,column:int):
        super().__init__()
        self.exp=exp
        self.bloque=bloque
        self.line=line
        self.column=column
    def ejecutar(self, driver: Driver, ts: Enviroment):
        t_exp = self.exp.getTipo(driver, ts)
        v_exp=self.exp.getValor(driver,ts)
        if t_exp!=Tipos.ERROR and t_exp==Tipos.BOOLEAN:
            while(v_exp):
                Newts = Enviroment(ts, 'While')
                for element in self.bloque:
                    #si viene alguna de estas instrucciones cambiar el flujo
                    if isinstance(element, Break):
                        return
                    elif isinstance(element, Continue):
                        break;
                    elif isinstance(element, Return):
                        print("Error, existe return afuera de una funcion")
                        error = "Error, existe return afuera de una funcion"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                          columna=self.column)
                        return
                    rInst=element.ejecutar(driver,Newts);

                    #si el resultado de ejecutar la instruccion devuelve alguno de estos cambiar el flujo
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
                t_exp = self.exp.getTipo(driver, ts)
                v_exp=self.exp.getValor(driver,ts)
                if t_exp == Tipos.ERROR and t_exp != Tipos.BOOLEAN:
                    print("La expresion da error o no es booleana")
                    error = "La expresion da error o no es booleana"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
                    return
        else:
            print("La expresion da error o no es booleana")
            error = "La expresion da error o no es booleana"
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
            return

    def generarC3d(self,ts,ptr:int):
        self.generator.addComment("While Instruction")
        self.exp.generator = self.generator
        loop = self.generator.newLabel()
        trueLabel=self.generator.newLabel()
        falseLabel=self.generator.newLabel()
        self.exp.trueLabel = trueLabel
        self.exp.falseLabel = falseLabel

        self.generator.addLabel(loop)
        vCondicion:ValC3d = self.exp.generarC3d(ts,ptr)

        if (vCondicion.tipo == Tipos.BOOLEAN):
            self.generator.addLabel(vCondicion.trueLabel)

            newEnv = Enviroment(ts,"While Bloque")
            self.generator.addNextStack(index=str(ts.size))
            for ins in self.bloque:
                ins.generator = self.generator
                ins.generarC3d(newEnv,ptr)
            self.generator.addBackStack(index=str(ts.size))
            self.generator.addGoto(loop)
            self.generator.addLabel(vCondicion.falseLabel)
        else:
            print("La expresion no es booleana")
        self.generator.addComment("End While")
