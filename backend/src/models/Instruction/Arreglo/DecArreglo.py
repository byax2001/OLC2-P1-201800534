from models.Abstract.Instruction import Instruccion
from models.Abstract.Expresion import Expresion
from models.Driver import Driver
from models.TablaSymbols.Enviroment import Enviroment
from models.Expresion.Vector.Vector import Vector
from models.Expresion.Vector.VectorC3d import VectorC3d
from models.TablaSymbols.Symbol import Symbol
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d
from models.TablaSymbols.SymC3d import SymC3d
from models.Expresion.Id import Id

class DecArreglo(Instruccion):
    def __init__(self,mut:bool,id:str,arrDimensional:Expresion,array:Expresion,line:int,column:int):
        super().__init__()
        self.mut=mut
        self.id=id
        self.arrDim=arrDimensional
        self.array=array
        self.line=line
        self.column=column
        self.tacceso = 0 #publico por default
        # DECLARACION CON PASO DE PARAMETRO
        self.dec_paso_parametro = False
        # cambio de entorno
        self.puntero_entorno_nuevo = ""
        self.en_funcion = False

    def ejecutar(self, driver: Driver, ts: Enviroment):
        if ts.buscarActualTs(self.id)==None:
            if self.arrDim!=None:
                id=self.id
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
                        B_datos().appendVar(id=self.id, t_simbolo=symbol.tsimbolo, t_dato=symbol.tipo, ambito=ts.env,
                                          fila=self.line, columna=self.column)

                        print("Arreglo declarado")
                    else:
                        print(f"Error las dimensionales del array y su contenido no concuerdan linea: {self.line}")
                        error = "Error las dimensionales del array y su contenido no concuerdan"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                          columna=self.column)
                else:
                    print(f"Error el tipo de dimensional y el del array no concuerdan linea: {self.line}")
                    error = "Error el tipo de dimensional y el del array no concuerdan"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
            else:
                t_array = self.array.getTipo(driver, ts)
                v_array = self.array.getValor(driver, ts)
                nvector = Vector(vec=v_array, stateCap=False, capacity=0)
                symbol = Symbol(mut=self.mut, id=self.id, value=nvector, tipo_simbolo=1, tipo=t_array, line=self.line,
                                column=self.column,tacceso=self.tacceso)
                ts.addVar(self.id, symbol)
                print("Arreglo declarado")

                B_datos().appendVar(id=self.id,t_simbolo=symbol.tsimbolo,t_dato=symbol.tipo,ambito=ts.env,fila=self.line,columna=self.column)

        else:
            print(f"Error el array ya ha sido declarado con anterioridad linea: {self.line}")
            error = "Error el array ya ha sido declarado con anterioridad "
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)

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
    def generarC3d(self,ts:Enviroment,ptr):
        self.generator.addComment(f"Declaracion de arreglo: {self.id}")
        Puntero = "P"
        if self.en_funcion:
            Puntero = self.puntero_entorno_nuevo
        if ts.buscarActualTs(self.id)==None:
            if self.arrDim==None:
                self.array.generator = self.generator
                array:ValC3d=self.array.generarC3d(ts,ptr)
                profundity = array.prof_array
                if not isinstance(self.array,Id):
                    profundity = profundity+1
                nvector=VectorC3d(vec=array.valor, profundidad=profundity)
                print(f"profundidad: {profundity}")
                symbol=Symbol(mut=self.mut,id=self.id,value=nvector,tipo_simbolo=1,tipo=array.tipo,
                              line=self.line,column=self.column,tacceso=self.tacceso,position=ts.size)
                symbol.paso_parametro = self.dec_paso_parametro  # por si acaso es una declaracion con paso de parametro

                rDec:SymC3d=ts.addVar(self.id, symbol)
                aux_index=self.generator.newTemp()
                self.generator.addExpression(target=aux_index, left=Puntero, right=str(rDec.position), operator="+")
                self.generator.addSetStack(index=aux_index, value=array.valor)  # Stack[(int)pos]= val
            else:
                self.arrDim.generator= self.array.generator = self.generator
                arrDim:ValC3d=self.arrDim.generarC3d(ts,ptr)
                array:ValC3d=self.array.generarC3d(ts,ptr)
                profundity=array.prof_array
                if not isinstance(self.array,Id):
                    profundity = profundity +1
                nvector = VectorC3d(vec=array.valor, profundidad=profundity)
                symbol=Symbol(mut=self.mut,id=self.id,value=nvector,tipo_simbolo=1,tipo=arrDim.tipo,
                              line=self.line,column=self.column,tacceso=self.tacceso,position=ts.size)
                symbol.paso_parametro = self.dec_paso_parametro  # por si acaso es una declaracion con paso de parametro

                rDec:SymC3d=ts.addVar(self.id, symbol)
                aux_index=self.generator.newTemp()
                self.generator.addExpression(target=aux_index, left=Puntero, right=str(rDec.position), operator="+")
                self.generator.addSetStack(index=aux_index, value=array.valor)  # Stack[(int)pos]= val
        else:
            error="variable ya declarada"
            print(error)