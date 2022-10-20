from models.Abstract.Instruction import Instruccion
from models.TablaSymbols.Enviroment import Enviroment
from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Symbol import Symbols
from models.TablaSymbols.Tipos import Tipos
from models.Instruction.Return import Return
from models.Instruction.Continue import Continue
from models.Instruction.Break import Break
from models.Expresion.Id import Id
from models import Driver
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d

class Call(Instruccion):
    def __init__(self,id:str,cExp:[Expresion],line:int,column:int):
        super().__init__()
        self.value=None
        self.tipo=None
        self.id=id
        self.cExp=cExp
        self.line=line
        self.column=column
        self.instancia=0
    def ejecutar(self, driver: Driver, ts: Enviroment):
        self.value=None
        self.tipo=None
        self.instancia = 0
        self.getTipo(driver, ts)
        self.getValor(driver,ts)

    def getValor(self, driver: Driver, ts: Enviroment):
        self.instancia+=1
        if self.value==None and self.tipo==None:
            newts=Enviroment(ts,"Funcion")
            newts2=Enviroment(newts,"BloqueFuncion")
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
                        try:
                            for declaracion in paramsFun:
                                declaracion.ejecutar(driver,newts)
                        except Exception as e:
                            print("Ocurrio un error  a la hora de declarar las variables para esta funcion")
                            error = "Ocurrio un error  a la hora de declarar las variables para esta funcion"
                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                              columna=self.column)
                        #bloque de la funcion -----------------------------------------
                        if symbol.tipo==Tipos.VOID:
                            for instruccion in instFun:
                                if isinstance(instruccion,Return):
                                    if instruccion.ejecutar(driver,newts2)!=None:
                                        print("Error se intenta retornar algo en una funcion Void")
                                        error = "Error se intenta retornar algo en una funcion Void"
                                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                                          columna=self.column)

                                elif isinstance(instruccion,Continue) or isinstance(instruccion,Break):
                                    print("Error se esta intentado usar Break o Continue en una funcion")
                                    error = "Error se esta intentado usar Break o Continue en una funcion"
                                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                                      columna=self.column)

                                rInst=instruccion.ejecutar(driver,newts2)

                                if isinstance(rInst,Return):
                                    if rInst.ejecutar(driver,newts2)!=None:
                                        print("Error se intenta retornar algo en una funcion Void")
                                        error = "Error se intenta retornar algo en una funcion Void"
                                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                                          columna=self.column)

                                elif isinstance(rInst,Continue) or isinstance(rInst,Break):
                                    print("Error se esta intentado usar Break o Continue en una funcion")
                                    error = "Error se esta intentado usar Break o Continue en una funcion"
                                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                                      columna=self.column)

                            self.value=None
                            self.tipo=Tipos.ERROR
                        else: #FUCIONES QUE RETORNAN VALORES-----------------------------------------------
                            for instruccion in instFun:

                                if isinstance(instruccion, Return):
                                    exp=instruccion.ejecutar(driver,newts2)
                                    if exp== None:
                                        print("Error no se intenta retornar algo en la funcion que debe retornar")
                                        error = "Error no se intenta retornar algo en la funcion que debe retornar"
                                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                                          columna=self.column)

                                    else:
                                        self.tipo=exp.getTipo(driver,newts2)
                                        valor=exp.getValor(driver,newts2)
                                        if self.tipo==symbol.tipo:  #la funcion debe de retornar un valor del mismo tipo el que fue declarada
                                            self.value=valor
                                            if isinstance(exp,Id) and type(valor)==list:
                                                self.value=exp.getVector(driver,newts2)
                                        elif symbol.tipo==Tipos.ARREGLO and type(valor)==list: #symbol.tipo tipo del valor de la funcion a retornar
                                            self.value = valor
                                        else:
                                            print("La funcion no esta retornando un valor del mismo tipo que esta")
                                            error = "La funcion no esta retornando un valor del mismo tipo que esta"
                                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                                              columna=self.column)
                                        break
                                elif isinstance(instruccion, Continue) or isinstance(instruccion, Break):
                                    print("Error se esta intentado usar Break o Continue en una funcion")
                                    error = "Error se esta intentado usar Break o Continue en una funcion"
                                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                                      columna=self.column)

                                print(f"-----------------------{self.id if self.id!=None else 2}")
                                rInst = instruccion.ejecutar(driver,newts2)

                                if isinstance(rInst, Return):
                                    print(symbol.tipo)
                                    exp = rInst.ejecutar(driver,newts2)
                                    if exp == None:
                                        print("Error no se intenta retornar algo en la funcion que debe retornar")
                                        error = "Error no se intenta retornar algo en la funcion que debe retornar"
                                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                                          columna=self.column)

                                    else:
                                        self.tipo = exp.getTipo(driver, newts2)
                                        valor=exp.getValor(driver, newts2)
                                        if self.tipo == symbol.tipo:
                                            self.value = valor
                                            break
                                            #simbol es un enum que contiene los tipos de variables
                                        elif symbol.tipo==Tipos.STRUCT and type(valor)==list: #symbol.tipo tipo del valor de la funcion a retornar
                                            self.value = valor
                                            break
                                        else:
                                            print("La funcion no esta retornando un valor del mismo tipo que esta")
                                            error = "La funcion no esta retornando un valor del mismo tipo que esta"
                                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                                              columna=self.column)

                                elif isinstance(rInst, Continue) or isinstance(rInst, Break):
                                    print("Error se esta intentado usar Break o Continue en una funcion")
                                    error = "Error se esta intentado usar Break o Continue en una funcion"
                                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                                      columna=self.column)

                    else:
                        print("el call no posee la cantidad de parametros adecuados que la funcion requiere ")
                        error = "el call no posee la cantidad de parametros adecuados que la funcion requiere"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                          columna=self.column)
                else:
                    print("la variable que se intenta ejecutar no es una funcion"+str(self.line))
                    error = "la variable que se intenta ejecutar no es una funcion"
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
            else:
                print("No ha sido declarada dicha funcion "+str(self.line))
                error = "No ha sido declarada dicha funcion"
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)

        return self.value

    def getTipo(self,driver,ts):
        self.resetInst()
        if self.value==None and self.tipo==None :
            self.getValor(driver,ts)  #en get valor se asigna tambien el valor de self.tipo
            if self.value==None: #si despues de eso sigue siendo None ocurrio un error
                self.tipo=Tipos.ERROR
        else:
            self.instancia+=1
        return self.tipo
    def resetInst(self):
        if self.instancia>1:
            self.instancia=0
            self.value=None
            self.tipo=None

    def generarC3d(self,ts:Enviroment,ptr:int):
        if self.id=="main":
            symbol = ts.buscar(self.id)
            insts=symbol.value[1]
            newEnv = Enviroment(anterior=ts,env="Call")
            for inst in insts:
                inst.generator = self.generator
                inst.generarC3d(newEnv,ptr+1)
        else:
            symbol = ts.buscar(self.id)
            if symbol!=None:
                self.generator.addComment(f"Llamada a funcion: {self.id}")
                newts = Enviroment(ts, "Funcion")
                newts.generator = self.generator
                newts.size=1 #para saltarse la primera posicion, pues ahi estara el valor del return
                newts.generator=ts.generator
                puntero_newEnv=ts.generator.newTemp()
                self.generator.addExpression(target=puntero_newEnv,left="P",right=str(ts.size),operator="+")
                #change expresion
                paramsFun = symbol.value[0]  # parametros de la funcion
                instFun = symbol.value[1]  # instrucciones de la funcion
                if len(self.cExp) == len(symbol.value[0]):  # el numero de parametros mandados
                    # por el call y los que necesita la funcion deben de ser iguales
                    x = 0
                    # ==============================Asignacion de expresiones para las declaraciones de la funcion=======================
                    for exp in self.cExp:  # expresiones enviados en el call
                        paramsFun[x].changeExp(exp)
                        x += 1
                    # ==============================Declaracion de parametros=======================
                    for declaracion in paramsFun:
                        declaracion.generarC3d(newts,ptr)
                else:
                    return ValC3d(valor="0",isTemp=False,tipo=Tipos.ERROR,tipo_aux=Tipos.ERROR)
                #crear funcion en c3d si no ha sido creada
                if symbol.func_create==False:
                    self.crear_funcC3d(instructions=instFun,ts=newts,ptr=ptr)
                    symbol.func_create=True
                    newts.actualizar(id=self.id,value=symbol)
                #LLAMADA
                self.generator.addNextStack(index=str(ts.size))
                self.generator.addCallFunc(self.id)
                self.generator.addBackStack(index=str(ts.size))
                #VALOR RETURN
                tmp_aux=self.generator.newTemp() #indice donde se encuentra el resultado del metodo
                tmp_return=self.generator.newTemp() #resultado del metodo
                self.generator.addExpression(target=tmp_aux,left="P",right=str(ts.size),operator="+")
                self.generator.addGetStack(target=tmp_return,index=tmp_aux)
                return ValC3d(valor=tmp_return,isTemp=True,tipo=self.tipo,tipo_aux=self.tipo)
            else:
                print("No ha sido declarada dicha funcion " + str(self.line))
                error = "No ha sido declarada dicha funcion"


    def crear_funcC3d(self,instructions,ts,ptr):
        exit_return=self.generator.newLabel()
        #CREACION DE LA FUNCION EN C3D
        code_func="void "+self.id + "(){{\n"
        i_aux1=len(self.generator.code)
        for inst in instructions:
            inst.generator=self.generator
            inst.generarC3d(ts,ptr)
        i_aux2=len(self.generator.code)
        #copiar lo que se almaceno en el arreglo code al string actual
        for i in range(i_aux1,i_aux2):
            code_func+=(self.generator.code[i]+"\n")
        #limpiar el arreglo code quitando el codigo que pertenece a la funcion
        for i in reversed(range(i_aux1,i_aux2)):  # reversed es para usar un rango a la inversa de n a 0
            self.generator.code.pop(i)
        code_func=code_func.replace("return_i",exit_return)
        code_func+=exit_return+":\n"
        code_func += f"return; \n"
        code_func += f"}}}} \n"
        self.generator.addCodeFunc(code=code_func)

