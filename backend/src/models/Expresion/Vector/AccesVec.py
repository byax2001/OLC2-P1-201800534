from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.Symbol import Symbols
from models.TablaSymbols.Tipos import Tipos
from BaseDatos.B_datos import B_datos


class AccesVec(Expresion):
    def __init__(self, id: str,cIndex:[Expresion],cIds:[str], line: int, column: int):
        self.value=None
        self.tipo=None
        self.id = id
        self.cIndex=cIndex
        self.cIds=cIds
        self.line = line
        self.column = column
        self.instancia=0
    def ejecutar(self,driver,ts):
        pass
    def getValor(self, driver, ts):
        self.instancia += 1
        if self.tipo==None and self.value==None:
            symbol = ts.buscar(self.id)
            vecIndex=[]
            for index in self.cIndex:
                tipo_index=index.getTipo(driver,ts)
                if tipo_index==Tipos.INT64 or tipo_index==Tipos.USIZE:  #cIndex= [expresion,expresion,expresion]
                    vecIndex.append(index.getValor(driver,ts))
                else:
                    print(f"Error: uno de los index no es un entero {self.line}")
                    error = "Error: uno de los index no es un entero "
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
                    return

            if symbol != None:  # si existe el vector, si ya fue declarado
                if symbol.tsimbolo == Symbols.VECTOR or symbol.tsimbolo==Symbols.ARREGLO:  # si lo que se llamo fue un vector o arreglo
                    vector = symbol.value
                    self.value = vector.acces(vecIndex) #Se llama al metodo declarado en la clase Vector para obtener el valor del elemento deseado
                                                            #con los indices especificados.
                    if self.value != None:
                            self.tipo = symbol.tipo
                    else:
                        #mensaje de error en el metoo del vector
                        self.tipo = Tipos.ERROR
                        #HASTA ACA TERMINARIA SI FUERA SOLO arreglo[0]
                        #pero si es arreglo[0].variable entonces hacer lo de abajo
                    if len(self.cIds)>0 and self.tipo==Tipos.STRUCT:
                        objeto:Enviroment=self.value
                        x = 0
                        for id in self.cIds:
                            objeto=objeto.buscar(id)
                            x += 1
                            if objeto.tipo != Tipos.STRUCT and x != len(self.cIds):
                                print("Error la variable no cuenta con tantos parametros anidados")
                                error = "Error la variable no cuenta con tantos parametros anidados"
                                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                                  columna=self.column)
                                return
                        self.value=objeto.value
                        self.tipo=objeto.tipo

                else:
                    print(f"Error Intento de obtener valor en una variable no vectorial  linea:{self.line} ")
                    error = "Error Intento de obtener valor en una variable no vectorial"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
            else:
                print(f"Error Intento de Insert en vector no declarado linea:{self.line} ")
                error = "Error Intento de Insert en vector no declarado linea"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        return self.value
    def getTipo(self, driver, ts):
        self.resetInst()
        if self.value==None and self.tipo==None:
            self.getValor(driver,ts)
            if self.value==None: #si despues de eso aun es None entonces da error al intentar obtener un valor
                self.tipo==Tipos.ERROR
        else:
            self.instancia+=1
        return self.tipo

    def resetInst(self):
        if self.instancia>1:
            self.instancia=0
            self.value=None
            self.tipo=None