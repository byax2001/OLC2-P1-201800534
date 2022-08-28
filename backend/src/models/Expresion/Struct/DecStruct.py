from models.Expresion.Expresion import Expresion
from models.Driver import Driver
from models.TablaSymbols.Enviroment import Enviroment
from models.Expresion.Struct.ExpStruct import ExpStruct
from models.Expresion.Struct.Struct import Struct
from models.TablaSymbols.Symbol import Symbol,Symbols
from models.TablaSymbols.Tipos import Tipos


class DecStruct(Expresion):
    def __init__(self, idStruct: str, expStruct:[ExpStruct], line: int, column: int):
        self.value=None
        self.tipo=None
        self.idSt=idStruct
        self.cExp=expStruct
        self.line=line
        self.column=column

    #  let id =     id       { var : valor , var2: valor }
    #      id      idStruct             expsStruct
    def getValor(self, driver, ts):  #lo que va a retornar va a ser un Enviromet o tabla ts a guardar
        newts = Enviroment(ts, "Struct")
        struct = ts.buscar(self.idSt)
        if struct != None:
            if struct.tipo == Tipos.STRUCT:
                st: Struct = struct.value
                if len(self.cExp) == st.getSize():
                    for exp in self.cExp:
                        changeExp = st.changeExp(exp.id, exp.exp)

                        if changeExp == False:
                            print(
                                "Error al asignar: la variable no existe en el struct solicitado o el tipo de valor no es igual al tipo  de la variable")
                            return
                    # mando a ejecutar el metodo en la clase Struct que ejecuta todas sus declaraciones
                    stateDecs = st.ejecutarDecs(driver, newts)
                    if stateDecs != None:  # si devuelve Falso y no None es que ocurrio un error al declarar
                        print("Ocurrio un error al intentar declarar una variable tipo struct")
                        self.value=None
                    # lo que guardara en las variables struct son enviroments nuevos donde se podra consultar las variables declaradas aqui para manipularlas en posteriores ocasiones
                    self.value=newts
                else:
                    print("No tiene la cantidad suficiente de variables declaradas para el struct")
                    self.value = None
            else:
                print("Error el id del struct a declarar en una variable pertenece al id de una variable no struct")
                self.value = None
        else:
            print("Intento de asignacion de un struct inexistente")
            self.value=None

    def getTipo(self, driver, ts):
        if self.value==None and self.tipo==None:
            self.getValor(driver,ts)
            if self.value==None:
                self.tipo=Tipos.ERROR
            else:
                self.tipo=Tipos.STRUCT
        return self.tipo

    def ejecutar(self, driver: Driver, ts: Enviroment):
        pass