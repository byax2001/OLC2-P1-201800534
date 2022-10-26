from models.Abstract.Instruction import Instruccion
from models.TablaSymbols.Enviroment import Enviroment
from models.Abstract import Expresion
from models import Driver
from models.TablaSymbols.ValC3d import ValC3d
from models.TablaSymbols.Tipos import Tipos
from BaseDatos.B_datos import B_datos

class Return(Instruccion):
    def __init__(self, exp: Expresion, line:int, column:int):
        self.exp=exp
        self.line = line
        self.column = column
    def ejecutar(self, driver: Driver, ts: Enviroment):
        if self.exp==None:
            return None
        else:
            return self.exp
    def generarC3d(self,ts,ptr:int):
        ts.generator=self.generator
        posCorret = self.SentTranferenciaC(ts, ["Funcion"])
        if posCorret==True:
            t_envAf = self.generator.newTemp()  # temporal con el tamaño necesario para regresar la pila a su estado en el inicio de la funcion
            self.generator.addExpAsign(target=t_envAf, right="0");
            envBucle: Enviroment = self.EnvMasCercanoContinue(ts, ["Funcion"], tmpA=t_envAf)
            tmp_index=self.generator.newTemp()
            if self.exp!=None:
                self.exp.generator=self.generator
                self.generator.addComment("Index de la pos de Return")

                exp:ValC3d=self.exp.generarC3d(ts,ptr)
                if exp.tipo!=Tipos.BOOLEAN or exp.tipo_aux in [Tipos.ARREGLO,Tipos.VECTOR]:
                    self.generator.addComment("Ingreso de valor a la Pos Return")
                    self.generator.addBackStack(index=str(t_envAf))  # PARA REGRESAR AL ENVIROMENT ANTERIOR al inicio de la funcion
                    self.generator.addExpression(target=tmp_index, left="P", right="0", operator="+")
                    self.generator.addSetStack(index=tmp_index, value=exp.valor)
                else:
                    self.generator.addComment("Ingreso de valor a la Pos Return")
                    lsalida = self.generator.newLabel()
                    self.generator.addLabel(exp.trueLabel)
                    self.generator.addBackStack(
                        index=str(t_envAf))  # PARA REGRESAR AL ENVIROMENT ANTERIOR al inicio de la funcion
                    self.generator.addExpression(target=tmp_index, left="P", right="0", operator="+")
                    self.generator.addSetStack(index=tmp_index, value="1")
                    self.generator.addGoto(lsalida)
                    self.generator.addLabel(exp.falseLabel)
                    self.generator.addBackStack(index=str(t_envAf))  # PARA REGRESAR AL ENVIROMENT ANTERIOR al inicio de la funcion
                    self.generator.addExpression(target=tmp_index, left="P", right="0", operator="+")
                    self.generator.addSetStack(index=tmp_index, value="0")
                    self.generator.addLabel(lsalida)
            self.generator.addCode("return_i")
        else:
            error = "Return no esta en una funcion"
            print(error)
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
