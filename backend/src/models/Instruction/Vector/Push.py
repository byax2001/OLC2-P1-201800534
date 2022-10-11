from models.Abstract.Instruction import Instruccion
from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Symbol import Symbols,Symbol
from models.Driver import Driver
from models.TablaSymbols.Enviroment import Enviroment
from BaseDatos.B_datos import B_datos
class Push(Instruccion):
    def __init__(self,id:str,exp:Expresion,line:int,column:int):
        super().__init__()
        self.id=id
        self.exp=exp
        self.line=line
        self.column=column
    def ejecutar(self, driver: Driver, ts: Enviroment):
        symbol=ts.buscar(self.id)
        if symbol!=None:
            if symbol.mut==True:
                if symbol.tsimbolo==Symbols.VECTOR:
                    v_exp=self.exp.getValor(driver,ts)
                    t_exp=self.exp.getTipo(driver,ts)
                    if v_exp!=None and t_exp!=Tipos.ERROR:
                        if t_exp==symbol.tipo:
                            vector=symbol.value
                            vector.push({"valor":v_exp,"tipo":t_exp})
                        else:
                            print(f"Error Intento de push de un valor con un tipo distinto al vector linea:{self.line} ")
                            error = "Error Intento de push de un valor con un tipo distinto al vector"
                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                              columna=self.column)
                    else:
                        print(f"Expresion causa error al intentar hacer push  linea:{self.line} ")
                        error = "Expresion causa error al intentar hacer push "
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                          columna=self.column)
                else:
                    print(f"Error Intento de push en una variable no vectorial  linea:{self.line} ")
                    error = "Error Intento de push en una variable no vectorial "
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
            else:
                print(f"Intento de Push en vector no muteable linea: {self.line}")
                error = "Intento de Push en vector no muteable "
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        else:
            print(f"Error Intento de push en vector no declarado linea:{self.line} ")
            error = "Error Intento de push en vector no declarado "
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
    def generarC3d(self,ts,ptr):
        symbol:Symbol = ts.buscar(self.id)
        if symbol != None:
            if symbol.mut == True:
                if symbol.tsimbolo==Symbols.VECTOR:
                    print()
                    # t_tam=inicioArray
                    # t_index=inicioArray+1 pos;
                    # tcont=0
                    # t_inewArr=H  //puntero del nuevo array
                    # Heap[H]=t_tam+1; //nuevo tamaño del nuevo array
                    # H=H+1
                    # loop:
                    #  if (tcont>=t_tam) goto Lsalida
                    #   taux=Heap[t_index]
                    #   Heap[H]=taux
                    #   H=H+1
                    #   t_index=t_index+1
                    #   tcont= tcont+1
                    # Lsalida:
                else:
                    error = "Se intenta hacer push a una variable que no es un vector"
                    print(error)
            else:
                error="Intento de cambio a un arreglo no muteable"
                print(error)
        else:
            error="No existe dicho arreglo"
            print(error)