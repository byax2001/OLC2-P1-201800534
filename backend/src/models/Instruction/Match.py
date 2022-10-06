from models.Abstract.Instruction import Instruccion
from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models import Driver
from models.Instruction.Brazo import Brazo
from BaseDatos.B_datos import B_datos
class Match(Instruccion):
    def __init__(self,exp:Expresion,lbrazos:[Brazo],default:[Instruccion],line:int,column:int):
        super().__init__()
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
                error = "Error: uno de los brazos tiene como expresion un tipo distinto a la expresion del match"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
                return None
        for brazo in self.listBrazos:
            CmpValores = brazo.CompararVexps(driver, new_ts,v_exp) #si alguno de los brazos tiene como cabecera la expresion solicitada en el match
            if(CmpValores):
                brazo.ejecutar(driver,new_ts) #ejecuta la instruccion del brazo
                return
        #si no se ejecuta ninguna de las instrucciones anteriores se ejecuta el default
        for instruccion in self.default:
            instruccion.ejecutar(driver,new_ts)
        return None
    def generarC3d(self,ts,ptr:int):
        self.generator.addComment("Match Instruction")
        lsalida=self.generator.newLabel()
        labels=[]
        expM=self.exp.generarC3d(ts,ptr)
        for brazo in self.listBrazos:
            brazo.generator=self.generator
            Lainst=self.generator.newLabel() #label con las instrucciones a ejecutar del brazo
            brazo.CmpExpB(expM=expM,Lainst=Lainst,ts=ts,ptr=ptr)
            labels.append(Lainst)
        self.generator.addComment("Default")
        for ins in self.default:
            ins.generator=self.generator
            ins.generarC3d(ts,ptr)
        self.generator.addComment("End default")
        self.generator.addGoto(lsalida)
        for x in range(len(self.listBrazos)):
            self.generator.addLabel(labels[x])
            self.listBrazos[x].generarC3d(ts,ptr)
            self.generator.addGoto(lsalida)

        self.generator.addLabel(lsalida)

