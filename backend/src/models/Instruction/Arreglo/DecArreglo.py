from models.Instruction.Instruction import Instruccion
from models.Expresion.Expresion import Expresion
from models.Driver import Driver
from models.TablaSymbols.Enviroment import Enviroment
from models.Expresion.Vector.Vector import Vector
from models.TablaSymbols.Symbol import Symbol
class DecArreglo(Instruccion):
    def __init__(self,mut:bool,id:str,arrDimensional:Expresion,array:Expresion,line:int,column:int):
        self.mut=mut
        self.id=id
        self.arrDim=arrDimensional
        self.array=array
        self.line=line
        self.column=column
        self.tacceso = 0 #publico por default
    def ejecutar(self, driver: Driver, ts: Enviroment):
        if ts.buscarActualTs(self.id)==None:
            if self.arrDim!=None:
                t_dim = self.arrDim.getTipo(driver, ts)
                v_dim = self.arrDim.getValor(driver,ts)
                t_array = self.array.getTipo(driver, ts)
                v_array = self.array.getValor(driver,ts)
                if t_dim==t_array:

                    arrCorrect=self.verifyArray(v_dim,v_array)
                    if arrCorrect==True:
                        #el array se declara como vector pues poseen metodos similares, sin embargo hay otros que no y estos estan asegurados
                        #para no usarse en arrays y solo en vectores
                        nvector=Vector(vec=v_array,stateCap=False,capacity=0)
                        symbol=Symbol(mut=self.mut,id=self.id,value=nvector,tipo_simbolo=1,tipo=t_dim,
                                      line=self.line,column=self.column,tacceso=self.tacceso)
                        ts.addVar(self.id,symbol)
                        print("Arreglo declarado")
                    else:
                        print(f"Error las dimensionales del array y su contenido no concuerdan linea: {self.line}")
                else:
                    print(f"Error el tipo de dimensional y el del array no concuerdan linea: {self.line}")
            else:
                t_array = self.array.getTipo(driver, ts)
                v_array = self.array.getValor(driver, ts)
                nvector = Vector(vec=v_array, stateCap=False, capacity=0)
                symbol = Symbol(mut=self.mut, id=self.id, value=nvector, tipo_simbolo=1, tipo=t_array, line=self.line,
                                column=self.column,tacceso=self.tacceso)
                ts.addVar(self.id, symbol)
                print("Arreglo declarado")
        else:
            print(f"Error el array ya ha sido declarado con anterioridad linea: {self.line}")


    def verifyArray(self,arrDim,arrayC):
        arrCorrect=True
        for dimensional in arrDim:#en anteriores metodos se aseguro que las dimensionales que vienen aca son enteras
            if type(arrayC)==list:
                if dimensional!=len(arrayC):  #si
                    arrCorrect=False
                    break
            else:  #si hay mas dimensionales que elementos lista en el array significa que la declaracion es erronea
                arrCorrect=False
                break
            arrayC=arrayC[0]["valor"]
        return arrCorrect
    def changeExp(self,exp:Expresion):
        self.array=exp

    def changeAcces(self,acceso:int):
        self.tacceso=acceso