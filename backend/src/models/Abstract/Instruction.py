from models.TablaSymbols.Enviroment import Enviroment
from Generator3D.Generator3D import Generator
from models.Driver import Driver


class Instruccion:
    def __init__(self) -> None:
        super().__init__()
        self.generator = Generator()
    def ejecutar(self, driver: Driver, ts: Enviroment):
        pass
    def generarC3d(self,ts,ptr):
        pass

    def SentTranferenciaC(self,ts:Enviroment,CiclosArr:list):
        while ts != None:
            if ts.env in CiclosArr:
                return True
            ts = ts.anterior
        return False

    #RETORNA EL ENVIROMENT MAS CERCANO, QUE CUMPLE CON LAS CARACTERISTICAS SOLICITADAS
    def EnvMasCercanoName(self,ts:Enviroment,CiclosArr:list):
        while ts != None:
            if ts.env in CiclosArr:
                return ts.env
            ts = ts.anterior
        return ""

    #RETORNA EL ENVIROMENT MAS CERCANO, QUE CUMPLE CON LAS CARACTERISTICAS SOLICITADAS
    def EnvMasCercanoContinue(self,ts:Enviroment,CiclosArr:list,tmpA):
        while ts != None:
            if ts.env in CiclosArr:
                return ts

            ts = ts.anterior
            if ts!=None:
                self.generator.addExpression(target=tmpA, left=tmpA, right=str(ts.size), operator="+")
        return None