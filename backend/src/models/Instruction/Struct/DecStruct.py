from models.Instruction.Instruction import Instruccion
from models.Driver import Driver
from models.TablaSymbols.Enviroment import Enviroment
from models.Expresion.Struct.ExpStruct import ExpStruct
from models.Expresion.Struct.Struct import Struct
from models.TablaSymbols.Symbol import Symbol,Symbols
from models.TablaSymbols.Tipos import Tipos

#ESTA INSTRUCCION YA NO SE USARA SE SUSTITUIRA POR DECLARACION NORMAL (let id igual EXPRESION)
#donde expresion sera esta declaracion de estruct pero con getvalor y get tipo
#"""DECSTRUCT : let id igual id llavea CONJEXP_STRUCT llavec
 #                   | let mut id igual id llavea CONJEXP_STRUCT llavec"""

class DecStruct(Instruccion):
    def __init__(self,mut, id, idStruct: str, expStruct:[ExpStruct], line: int, column: int):
        self.mut=mut
        self.id = id
        self.idSt=idStruct
        self.cExp=expStruct
        self.line=line
        self.column=column

    #  let id =     id       { var : valor , var2: valor }
    #      id      idStruct             expsStruct

    def ejecutar(self, driver: Driver, ts: Enviroment):
        newts=Enviroment(ts,"Struct")
        existe=ts.buscarActualTs(self.id)
        if existe==None:
            struct=ts.buscar(self.idSt)
            print(self.idSt)
            if struct!=None:
                if struct.tipo == Tipos.STRUCT:
                    st:Struct=struct.value
                    if len(self.cExp)==st.getSize():
                        for exp in self.cExp:
                            changeExp=st.changeExp(exp.id,exp.exp)

                            if changeExp==False:
                                print("Error al asignar: la variable no existe en el struct solicitado o el tipo de valor no es igual al tipo  de la variable")
                                return
                        #mando a ejecutar el metodo en la clase Struct que ejecuta todas sus declaraciones
                        stateDecs=st.ejecutarDecs(driver,newts)
                        if stateDecs!=None:  #si devuelve Falso y no None es que ocurrio un error al declarar
                            print("Ocurrio un error al intentar declarar una variable tipo struct")
                            return False
                        #lo que guardaran los structs son enviroments nuevos donde se podra consultar las variables en posteriores ocasiones
                        symbol=Symbol(mut=self.mut,id=self.mut,value=newts,tipo_simbolo=4,tipo=Tipos.STRUCT,line=self.line,column=self.column)
                        ts.addVar(self.id,symbol)
                        print("Variable struct declarada")
                    else:
                        print("No tiene la cantidad suficiente de variables declaradas para el struct")
                else:
                    print("Error el id del struct a declarar en una variable pertenece al id de una variable no struct")
            else:
                print("Intento de asignacion de un struct inexistente")
        else:
            print("Error la variable ya ha sido declarada")