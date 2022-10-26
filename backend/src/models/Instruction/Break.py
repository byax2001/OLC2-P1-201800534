from models.Abstract.Instruction import Instruccion
from models.TablaSymbols.Enviroment import Enviroment
from models.Abstract import Expresion
from models import Driver
from models.TablaSymbols.ValC3d import ValC3d
from models.TablaSymbols.Tipos import Tipos
from BaseDatos.B_datos import B_datos
class Break(Instruccion):
    def __init__(self, exp: Expresion, line:int, column:int):
        super().__init__()
        self.exp = exp
        self.linea = line
        self.columna = column
    def ejecutar(self, driver: Driver, ts: Enviroment):
        pass
    def getValor(self,driver,ts):
        return self.exp.getValor(driver,ts);
    def getTipo (self,driver,ts):
        return self.exp.getTipo(driver,ts)
    def generarC3d(self,ts:Enviroment,ptr):
        self.generator.addComment("Break")
        # que break este en un enviroment correcto (osea un ciclo)
        posCorret = self.SentTranferenciaC(ts,["Loop","While","ForIn"])
        if posCorret == True:
            result=ValC3d(valor="0",isTemp=False,tipo=Tipos.ERROR,tipo_aux=Tipos.ERROR)
            if self.exp!=None:
                self.exp.generator=self.generator
                result:ValC3d=self.exp.generarC3d(ts,ptr)
                if ts.env=="If":
                                                #tmpR = valorBreak
                                                # tn = val
                    self.generator.addExpAsign(target=str(ptr), right=str(result.valor))#tmp: temporal resultante
                    #retroceder al ambiente anterior: P = P-n

                else:
                    self.generator.addExpAsign(target=ptr, right=result.valor)
            t_envAc = self.generator.newTemp()  # temporal con el tamaño necesario para regresar la pila a su estado en el inicio del bucle
            #con el metodo EnvMasCercano t_envAc tiene el tamaño suficiente para regresar la pila al estado inicial
            #del bucle, por ultimo ya que se sale de este con break, se resta el enviroment anterior para
            #regresar la pila al estado anterior de entrar ahi.
            envBucle: Enviroment = self.EnvMasCercanoContinue(ts, ["Loop", "While", "ForIn"], tmpA=t_envAc)
            self.generator.addExpression(target=t_envAc, left=t_envAc, right=str(envBucle.anterior.size),operator="+")
            self.generator.addBackStack(t_envAc)

            self.generator.addCode("break_i")
            return result
        else:
            error = "Break no esta en un bucle"
            print(error)
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.linea,
                              columna=self.columna)