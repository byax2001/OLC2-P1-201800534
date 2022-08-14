from models.Instruction.Instruction import Instruccion
from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from  models import Driver
from models.Instruction.Brazo import Brazo
from models.TablaSymbols.Tipos import Tipos,definirTipo

class Match(Instruccion):
    def __init__(self,exp:Expresion,lbrazos:[Brazo],default:[Instruccion],line:int,column:int):
        self.exp=exp
        self.listBrazos=lbrazos
        self.default=default
        self.line=line
        self.column=column

    def ejecutar(self, driver: Driver, ts: Enviroment):
        v_exp=self.exp.getValor(driver,ts)
        t_exp=self.exp.getTipo(driver,ts)
        new_ts = Enviroment(ts, 'Match')
        #se revisa que todos los brazos tengan el mismo tipo de expresion que la expresion principal
        for brazo in self.listBrazos:
            CmpTipos=brazo.CompararTexps(driver,new_ts,t_exp) #Comparar tipos de la exp del match con los tipos de las exp del brazo
            if (not CmpTipos):
                print("Error: uno de los brazos tiene como expresion un tipo distinto a la expresion del match")
                return None

        for brazo in self.listBrazos:
            CmpValores = brazo.CompararVexps(driver, new_ts,v_exp)
            if(CmpValores):
                brazo.ejecutar(driver,new_ts) #ejecuta la instruccion del brazo
                return
        #si no se ejecuta ninguna de las instrucciones anteriores se ejecuta el default
        for instruccion in self.default:
            instruccion.ejecutar(driver,new_ts)
        return None
