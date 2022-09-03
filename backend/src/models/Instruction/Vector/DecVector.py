from models.Instruction.Instruction import Instruccion
from models.Expresion.Vector.vecI import vecI
from models.Expresion.Expresion import Expresion
from models.Expresion.Vector.Vector import Vector
from models.TablaSymbols.Symbol import Symbol
from models.TablaSymbols.Tipos import Tipos,getTipo
from models.Driver import Driver
from models.TablaSymbols.Enviroment import Enviroment
#dec vector vacio
class DecVector(Instruccion):
    def __init__(self,mut:bool,id,tipo, vecI:vecI,capacity:Expresion,line:int,column:int):
        self.id=id
        self.mut = mut
        self.vecI=vecI
        self.capacity=capacity
        self.tipo =getTipo(tipo) if tipo!=None else None
        self.line=line
        self.column=column
        self.tacceso = 0  #publico por default
    def ejecutar(self, driver: Driver, ts: Enviroment):
        existe=ts.buscarActualTs(self.id)
        if existe==None:
            if self.vecI!=None and self.capacity==None:  #se creo el vector con vec!----------
                tvec = self.vecI.getTipo(driver, ts)
                v_vec=self.vecI.getValor(driver,ts)
                if tvec!=Tipos.ERROR and v_vec!=None:

                    if self.tipo==None:
                        newVec=Vector(vec=v_vec,stateCap=False,capacity=0)
                        symbol=Symbol(mut=self.mut,id=self.id,value=newVec,tipo_simbolo=3,tipo=tvec,line=self.line,
                                      column=self.column,tacceso=self.tacceso)
                        ts.addVar(self.id,symbol)
                        print("Se declaro un vector con \"vec!\"")
                    else:
                        if self.tipo==tvec:
                            newVec = Vector(vec=v_vec, stateCap=False, capacity=0)
                            symbol = Symbol(mut=self.mut, id=self.id, value=newVec, tipo_simbolo=3, tipo=tvec,
                                            line=self.line,
                                            column=self.column, tacceso=self.tacceso)
                            ts.addVar(self.id, symbol)
                            print("Se declaro un vector con \"vec!\"")
                        else:
                            "el tipo de variable declarado y de vec! no son iguales"
                else:
                    print("declaracion vec! dio error")
            elif self.capacity!=None:  #con capacity-------------------------------------------
                tcap = self.capacity.getTipo(driver, ts)
                cap=self.capacity.getValor(driver,ts)
                if tcap==Tipos.INT64 or tcap==Tipos.USIZE:
                    vec=[]
                    newVec=Vector(vec=vec,stateCap=True,capacity=cap)
                    symbol = Symbol(mut=self.mut, id=self.id, value=newVec, tipo_simbolo=3, tipo=self.tipo,
                                    line=self.line,column=self.column,tacceso=self.tacceso)
                    ts.addVar(self.id, symbol)
                    print("Se declaro un vector con \"with_capacity()\"")
                else:
                    print(f"Error la capacidad indicada no es un entero linea: {self.line}")
            else:  #con new--------------------------------------------------------------------
                newVec = Vector(vec=[], stateCap=False, capacity=0)
                symbol = Symbol(mut=self.mut, id=self.id, value=newVec, tipo_simbolo=3, tipo=self.tipo,
                                line=self.line,column=self.column,tacceso=self.tacceso)
                ts.addVar(self.id, symbol)
                print("Se declaro un vector con \"new()\"")
        else:
            print(f"La id del vector a declarar ya ha sido declarado con anterioridad linea: {self.line}")

    def rVector(self,tipo,nveces):
        vector=[]
        valor=self.valueDefault(tipo)
        for x in range(nveces):
            vector.append({"valor":valor,"tipo":tipo})
        return vector

    def valueDefault(self, tipo:Tipos):
        if(tipo==Tipos.INT64):
            return 0
        elif(tipo==Tipos.FLOAT64):
            return 0.0
        elif (tipo==Tipos.BOOLEAN):
            return False
        elif (tipo==Tipos.STR):
            return ""
        elif (tipo==Tipos.STRING):
            return ""
            return ""
        elif (tipo==Tipos.CHAR):
            return "\0"
    def changeExp(self,exp:Expresion):
        self.vecI=exp

    def changeAcces(self,acceso:int):
        self.tacceso=acceso