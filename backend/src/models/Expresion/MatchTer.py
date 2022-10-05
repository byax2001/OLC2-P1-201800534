from models.Abstract.Expresion import Expresion
from models.Expresion.BrazoTer import BrazoTer
from models.TablaSymbols.Tipos import Tipos
from BaseDatos.B_datos import B_datos
from  models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.ValC3d import ValC3d
class MatchTer(Expresion):
    def __init__(self, exp:Expresion,brazos:[BrazoTer],default:[Expresion], line: int, column: int):
        super().__init__()
        self.tipo=None
        self.value=None
        self.exp=exp
        self.brazos=brazos
        self.default=default
        self.line = line
        self.column = column

    def getValor(self, driver, ts):
        v_exp= self.exp.getValor(driver,ts)
        t_exp=self.exp.getTipo(driver,ts)
        #Revisar que todas las expresiones para decidir que brazo usar sean del mismo tipo al de la expresion del match
        for element in self.brazos:
            CmpTipos=element.CompararTexps(driver,ts,t_exp)
            if(not CmpTipos):
                print("Error: uno de los brazos tiene como expresion un tipo distinto a la expresion del match")
                error = "Error: uno de los brazos tiene como expresion un tipo distinto a la expresion del match"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
                return None
        #Revisar que todos los brazos retornen un mismo valor
        if(len(self.brazos)>=2):
            firstE=self.brazos[0]
            for element in self.brazos:
                if element.getTipo(driver,ts)!=firstE.getTipo(driver,ts):
                    print("Un brazo retorna una expresion de distinto tipo al resto")
                    error = "Un brazo retorna una expresion de distinto tipo al resto"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
                    return None
            if self.default.getTipo(driver, ts) != firstE.getTipo(driver, ts):
                print("El brazo default retorna una expresion de distinto tipo al resto")
                error = "El brazo default retorna una expresion de distinto tipo al resto"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
                return None
        #Retornar el valor del brazo con la misma expresion que la del match ternario
        for element in self.brazos:
            if element.CompararVexps(driver,ts,v_exp):
                return element.getValor(driver,ts)
        return self.default.getValor(driver,ts)

    def getTipo(self, driver, ts):
        t_exp = self.exp.getTipo(driver, ts)
        v_exp = self.exp.getValor(driver, ts)
        # Revisar que todas las expresiones para decidir que brazo usar sean del mismo tipo al de la expresion del match
        for element in self.brazos:
            CmpTipos = element.CompararTexps(driver, ts, t_exp)
            if (not CmpTipos):
                print("Error: uno de los brazos tiene como expresion un tipo distinto a la expresion del match")
                error = "Error: uno de los brazos tiene como expresion un tipo distinto a la expresion del match"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
                return Tipos.ERROR
        # Revisar que todos los brazos retornen un mismo valor
        if (len(self.brazos) >= 2):
            firstE = self.brazos[0]
            for element in self.brazos:
                if element.getTipo(driver, ts) != firstE.getTipo(driver, ts):
                    print("Un brazo retorna una expresion de distinto tipo al resto")
                    error = "Un brazo retorna una expresion de distinto tipo al resto"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
                    return Tipos.ERROR
            if self.default.getTipo(driver, ts) != firstE.getTipo(driver, ts):
                print("El brazo default retorna una expresion de distinto tipo al resto")
                error = "El brazo default retorna una expresion de distinto tipo al resto"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
                return Tipos.ERROR
        # Retornar el tipo de dato que todos los brazos y default tienen
        return self.default.getTipo(driver, ts)
    def ejecutar(self, driver, ts):
        """En la mayoria de expresiones no realiza nada"""
        pass

    def generarC3d(self,ts,ptr:int):
        tmpr=self.generator.newTemp()
        vret = ValC3d(valor=tmpr,isTemp=True,tipo=Tipos.ERROR,tipo_aux=Tipos.ERROR)
        lsalida = self.generator.newLabel()
        labels = []
        expM = self.exp.generarC3d(ts, ptr)

        for brazo in self.brazos:
            brazo.generator = self.generator
            Lainst = self.generator.newLabel()  # label con las instrucciones a ejecutar del brazo
            brazo.CmpExpB(expM=expM, Lainst=Lainst, ts=ts, ptr=ptr)
            labels.append(Lainst)
        # default
        self.default.generator = self.generator
        result: ValC3d = self.default.generarC3d(ts, ptr)
        self.generator.addExpAsign(target=tmpr, right=result.valor)
        self.generator.addGoto(lsalida)
        # ----------------------
        for x in range(len(self.brazos)):
            self.generator.addLabel(labels[x])
            result:ValC3d=self.brazos[x].generarC3d(ts, ptr,tmpr)
            if x==0:
                vret.tipo=result.tipo
                vret.tipo_aux=result.tipo_aux
                vret.trueLabel=self.trueLabel
                vret.falseLabel=self.falseLabel
            self.generator.addGoto(lsalida)
        self.generator.addLabel(lsalida)
        return vret