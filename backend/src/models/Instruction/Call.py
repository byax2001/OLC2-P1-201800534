from models.Instruction.Instruction import Instruccion
from models.TablaSymbols.Enviroment import Enviroment
from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Symbol import Symbols
from models.TablaSymbols.Tipos import Tipos
from models.Instruction.Return import Return
from models.Instruction.Continue import Continue
from models.Instruction.Break import Break
from models import Driver

class Call(Instruccion):
    def __init__(self,id:str,cExp:[Expresion],line:int,column:int):
        self.value=None
        self.tipo=None
        self.id=id
        self.cExp=cExp
        self.line=line
        self.column=column
    def ejecutar(self, driver: Driver, ts: Enviroment):
        self.getValor(driver,ts);
    def getValor(self, driver: Driver, ts: Enviroment):
        if self.value==None and self.tipo==None:
            newts=Enviroment(ts,"Funcion")
            symbol=ts.buscar(self.id);
            if symbol!=None:
                if symbol.tsimbolo==Symbols.FUNCION:
                    paramsFun=symbol.value[0]  #parametros de la funcion
                    instFun=symbol.value[1]    #instrucciones de la funcion
                    if len(self.cExp)==len(symbol.value[0]): #el numero de parametros mandados por el call y los que necesita la funcion deben de ser iguales
                        x=0
                        # ==============================Asignacion de expresiones para las declaraciones de la funcion=======================
                        for exp in self.cExp:  #expresiones enviados en el call
                            paramsFun[x].changeExp(exp)
                            x+=1

                        #==============================Declaracion de parametros=======================
                        for declaracion in paramsFun:
                            declaracion.ejecutar(driver,newts)

                        if symbol.tipo==Tipos.VOID:
                            for instruccion in instFun:
                                if isinstance(instruccion,Return):
                                    if instruccion.ejecutar(driver,newts)!=None:
                                        print("Error se intenta retornar algo en una funcion Void")
                                        return
                                elif isinstance(instruccion,Continue) or isinstance(instruccion,Break):
                                    print("Error se esta intentado usar Break o Continue en una funcion")
                                    return
                                rInst=instruccion.ejecutar(driver,newts)

                                if isinstance(rInst,Return):
                                    if rInst.ejecutar(driver,newts)!=None:
                                        print("Error se intenta retornar algo en una funcion Void")
                                        return
                                elif isinstance(rInst,Continue) or isinstance(rInst,Break):
                                    print("Error se esta intentado usar Break o Continue en una funcion")
                                    return
                        else: #FUCIONES QUE RETORNAN VALORES-----------------------------------------------
                            for instruccion in instFun:
                                if isinstance(instruccion, Return):
                                    exp=instruccion.ejecutar(driver,newts)
                                    if exp== None:
                                        print("Error no se intenta retornar algo en la funcion que debe retornar")
                                        return
                                    else:
                                        self.tipo=exp.getTipo(driver,newts)
                                        if self.tipo==symbol.tipo:  #la funcion debe de retornar un valor del mismo tipo el que fue declarada
                                            self.value=exp.getValor(driver,newts)
                                        else:
                                            print("La funcion no esta retornando un valor del mismo tipo que esta")
                                            return
                                elif isinstance(instruccion, Continue) or isinstance(instruccion, Break):
                                    print("Error se esta intentado usar Break o Continue en una funcion")
                                    return
                                rInst = instruccion.ejecutar(driver,newts)

                                if isinstance(rInst, Return):
                                    exp = rInst.ejecutar(driver,newts)
                                    if exp == None:
                                        print("Error no se intenta retornar algo en la funcion que debe retornar")
                                        return
                                    else:
                                        self.tipo = exp.getTipo(driver, newts)
                                        if self.tipo == symbol.tipo:
                                            self.value = exp.getValor(driver, newts)
                                        else:
                                            print("La funcion no esta retornando un valor del mismo tipo que esta")
                                            return
                                elif isinstance(rInst, Continue) or isinstance(rInst, Break):
                                    print("Error se esta intentado usar Break o Continue en una funcion")
                                    return
                    else:
                        print("el call no posee la cantidad de parametros adecuados que la funcion requiere ")
                else:
                    print("la variable que se intenta ejecutar no es una funcion"+str(self.line))
            else:
                print("No ha sido declarada dicha funcion "+str(self.line))
        return self.value

    def getTipo(self,driver,ts):
        if self.value==None and self.tipo==None :
            self.getValor(driver,ts)  #en get valor se asigna tambien el valor de self.tipo
            if self.value==None: #si despues de eso sigue siendo None ocurrio un error
                self.tipo=Tipos.ERROR
            return self.tipo
        else:
            return self.tipo