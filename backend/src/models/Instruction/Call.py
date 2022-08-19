from models.Instruction.Instruction import Instruccion
from models.TablaSymbols.Enviroment import Enviroment
from models.Instruction.Declaracion import Declaracion
from models.TablaSymbols.Symbol import Symbols
from models.TablaSymbols.Tipos import Tipos
from models.Instruction.Return import Return
from models.Instruction.Continue import Continue
from models.Instruction.Break import Break
from models import Driver

class Call(Instruccion):
    def __init__(self,id:str,parametros:[Declaracion],line:int,column:int):
        self.value=None
        self.tipo=None
        self.id=id
        self.params=parametros
        self.line=line
        self.column=column
    def ejecutar(self, driver: Driver, ts: Enviroment):
        #newts=Enviroment(ts,"Funcion")
        self.getValor(driver,ts);
    def getValor(self, driver: Driver, ts: Enviroment):
        symbol=ts.buscar(self.id);
        if symbol!=None:
            if symbol.tsimbolo==Symbols.FUNCION:
                paramsFun=symbol.value[0]
                instFun=symbol.value[1]
                if len(self.params)==len(symbol.value[0]):
                    x=0
                    # ==============================Asignacion de parametros=======================
                    for param in self.params:  #parametros enviados en el call
                        if not paramsFun[x].changeExp(param,driver,ts): #si no se logro cambiar changExp retornara False
                            print("Error uno de los parametros no coinciden de tipo con el tipo de variable declarada")
                            return
                        x+=1

                    #==============================Declaracion de parametros=======================
                    for param in paramsFun:
                        param.ejecutar(driver,ts)
                    #==============================Declaracion de parametros=======================
                    if symbol.tipo==Tipos.VOID:
                        for instruccion in instFun:
                            if isinstance(instruccion,Return):
                                if instruccion.getValor(driver,ts)!=None:
                                    print("Error se intenta retornar algo en una funcion Void")
                                    return
                            elif isinstance(instruccion,Continue) or isinstance(instruccion,Break):
                                print("Error se esta intentado usar Break o Continue en una funcion")

                            rInst=instruccion.ejecutar(driver,ts)

                            if isinstance(rInst,Return):
                                if instruccion.getValor(driver,ts)!=None:
                                    print("Error se intenta retornar algo en una funcion Void")
                                    return
                            elif isinstance(rInst,Continue) or isinstance(rInst,Break):
                                print("Error se esta intentado usar Break o Continue en una funcion")
                                return
                    else: #FUCIONES QUE RETORNAN VALORES-----------------------------------------------
                        for instruccion in instFun:
                            if isinstance(instruccion, Return):
                                exp=instruccion.ejecutar(driver, ts)
                                if exp== None:
                                    print("Error no se intenta retornar algo en la funcion que debe retornar")
                                    return
                                else:
                                    self.tipo=exp.getTipo(driver,ts)
                                    if self.tipo==symbol.tipo:
                                        self.value=exp.getValor(driver,ts)
                                    else:
                                        print("La funcion no esta retornando un valor del mismo tipo que esta")
                            elif isinstance(instruccion, Continue) or isinstance(instruccion, Break):
                                print("Error se esta intentado usar Break o Continue en una funcion")

                            rInst = instruccion.ejecutar(driver, ts)

                            if isinstance(rInst, Return):
                                exp = rInst.ejecutar(driver, ts)
                                if exp == None:
                                    print("Error no se intenta retornar algo en la funcion que debe retornar")
                                    return
                                else:
                                    self.tipo = exp.getTipo(driver, ts)
                                    if self.tipo == symbol.tipo:
                                        self.value = exp.getValor(driver, ts)
                                    else:
                                        print("La funcion no esta retornando un valor del mismo tipo que esta")
                            elif isinstance(rInst, Continue) or isinstance(rInst, Break):
                                print("Error se esta intentado usar Break o Continue en una funcion")
                                return
                        print() #debe de devolver algo
                else:
                    print("el call no posee la cantidad de parametros adecuados que la funcion requiere ")
            else:
                print("la variable que se intenta ejecutar no es una funcion"+str(self.line))
        else:
            print("No ha sido declarada dicha funcion "+str(self.line))
        return self.value

    def getTipo(self,driver,ts):
        if self.value==None:
            self.getValor(driver,ts)  #en get valor se asigna tambien el valor de self.tipo
            if self.value==None:
                self.tipo=Tipos.ERROR
            return self.tipo
        else:
            return self.tipo