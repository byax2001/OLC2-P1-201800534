from models.Abstract.Instruction import Instruccion
from models.TablaSymbols.Enviroment import Enviroment

class Continue(Instruccion):
    def __init__(self,line:int, column:int):
        super().__init__()
        self.linea = line
        self.columna = column
    def ejecutar(self, driver, ts):
        pass

    def v_uso_correcto(self,ts):
        if ts.env != "Loop" or ts.env != "While" or ts.env != "ForIn" or ts.env != "If":
            print("Error continue en un ambito que no es loop")
    def generarC3d(self,ts,ptr):
        self.generator.addComment("Continue")


        posCorret = self.SentTranferenciaC(ts, ["Loop", "While", "ForIn"])
        if posCorret==True: #100% seguridad que el continue vendra en un bucle si no, no se ejecutara lo siguiente solo el error
            t_envAc=self.generator.newTemp()#temporal con el tamaño necesario para regresar la pila a su estado en el inicio del bucle
            self.generator.addExpAsign(target=t_envAc,right="0");
            envBucle: Enviroment = self.EnvMasCercanoContinue(ts, ["Loop", "While", "ForIn"],tmpA=t_envAc)

            #EN EL WHILE SI HAY QUE SALIRSE DEL ENVIROMENT DE ESTE, PUES LAS CONDICIONES SE VERIFICAN CON EL ENV ANTERIOR
            if self.EnvMasCercanoName(ts,["Loop","While","ForIn"]) == "While":
                self.generator.addExpression(target=t_envAc,left=t_envAc,right=str(envBucle.anterior.size),operator="+")
            self.generator.addBackStack(index=str(t_envAc)) #PARA REGRESAR AL ENVIROMENT ANTERIOR, recordar que fijo vendra adentro de un bucle en esta parte
            self.generator.addCode("continue_i ")
        else:
            error = "Continue no esta en un bucle"
            print(error)