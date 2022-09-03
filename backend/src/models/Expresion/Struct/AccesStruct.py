from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Enviroment import Enviroment
class AccesStruct(Expresion):
    def __init__(self,idPrincipal:str,cIds:[str],line:int,column:int):
        self.value=None
        self.tipo=None
        self.idPrincipal=idPrincipal
        self.cId=cIds
        self.line=line
        self.column=column
        self.instancia=0

    def getValor(self, driver, ts:Enviroment):
        self.instancia+=1
        if self.value == None and self.tipo == None:
            varSt=ts.buscar(self.idPrincipal)
            if varSt!=None:
                if varSt.tipo==Tipos.STRUCT:
                    env_struct=varSt.value # el valor de cada variable objeto struct es un enviroment el cual se consulta
                    for x in range(len(self.cId)):
                        env = env_struct.buscar(self.cId[x])
                        if env!=None:
                            if env.tipo==Tipos.STRUCT:
                                env_struct=env.value
                                if x == (len(self.cId)-1): #devolvera un enviroment
                                    self.value=env.value
                                    self.tipo=env.tipo
                            else:
                                if x == (len(self.cId)-1): #devolvera un valor primitivo
                                    self.value=env.value
                                    self.tipo=env.tipo
                                else:
                                    self.value==None
                                    print("La variable no posee dichos componentes")
                        else:
                            print(f"Error dicho parametro no existe en el objeto {self.cId[x]}")
                else:
                    print("Error la variable a usar como objeto struct no lo es")
            else:
                print("Error variable a obtener valor no existe")
        return self.value

    def getTipo(self, driver, ts):
        self.resetInst()
        if self.value == None and self.tipo == None:
            self.getValor(driver, ts)
            if self.value == None:
                self.tipo = Tipos.ERROR
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