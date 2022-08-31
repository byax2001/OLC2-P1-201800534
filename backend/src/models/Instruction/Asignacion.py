from models.Instruction.Instruction import Instruccion
from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Symbol import Symbols
class Asignacion(Instruccion):
    def __init__(self,id:str,cIndex:[Expresion],cIds:[str],exp: Expresion, linea:int, columna:int):
        self.id=id
        self.cIndex=cIndex
        self.cIds=cIds
        self.exp = exp
        self.linea = linea
        self.columna = columna

    def ejecutar(self, driver, ts):
        Symbol=ts.buscar(self.id);
        if Symbol !=None:
            if(Symbol.mut==True):
                v_exp=self.exp.getValor(driver,ts)
                if v_exp!=None:
                    t_exp=self.exp.getTipo(driver,ts)
                    if Symbol.tipo == t_exp or Symbol.tipo==Tipos.STRUCT:
                        if len(self.cIndex)==0: #si es una asignacion normal
                            ts.actualizar(self.id,v_exp)
                        else: # si es la asignacion de un vector
                            if Symbol.tsimbolo==Symbols.ARREGLO or Symbol.tsimbolo==Symbols.VECTOR:
                                vecIndex=[]
                                for index in self.cIndex:
                                    tipo_index = index.getTipo(driver, ts)
                                    if tipo_index == Tipos.INT64 or tipo_index == Tipos.USIZE:  # cIndex= [expresion,expresion,expresion]
                                        vecIndex.append(index.getValor(driver, ts))
                                    else:
                                        print(f"Error: uno de los index no es un entero {self.line}")
                                        return
                                if len(self.cIds)==0:    # arreglo[0]= "hola"
                                    Symbol.value.updateVector(cIndex=vecIndex,valor=v_exp)
                                else: #arreglo[0].palabra= "hola"
                                    Symbol.value.updateVectorStruct(cIndex=vecIndex,cIds=self.cIds,valor=v_exp,tipo_val=t_exp)
                            else:
                                print("intento de hacer asignacion de vector a una variable que no lo es")

                    else:
                        print("El valor a asignar es de distinto tipo al de la variable")
                else:
                    print("El valor que se intenta asignar a la variable es None o da error")
            else:
                print("La variable que intenta cambiar no es muteable")
        else:
            print("No ha sido declarada dicha variable")