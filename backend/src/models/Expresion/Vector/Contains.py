from models.Abstract.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.Driver import Driver
from models.TablaSymbols.Tipos import Tipos,definirTipo
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.Symbol import Symbols,Symbol
from models.TablaSymbols.ValC3d import ValC3d
from models.Expresion.Operacion.Relacionales import Relacionales
from models.Expresion.AuxExp import AuxExp

class Contains(Expresion):
    def __init__(self, id: str, exp: Expresion, line: int, column: int):
        super().__init__()
        self.value=None
        self.tipo=None
        self.id = id
        self.exp = exp
        self.line = line
        self.column = column


    def ejecutar(self, driver: Driver, ts: Enviroment):
        self.getValor(driver,ts);

    def getValor(self, driver, ts):
        symbol = ts.buscar(self.id)
        t_exp = self.exp.getTipo(driver, ts)
        v_exp = self.exp.getValor(driver, ts)
        if symbol != None:  # si existe el vector, si ya fue declarado
            if symbol.tsimbolo == Symbols.VECTOR or symbol.tsimbolo==Symbols.ARREGLO:  # si lo que se llamo fue un vector o arreglo
                if t_exp != Tipos.ERROR and v_exp != None:
                    vector = symbol.value
                    self.value = vector.contains(v_exp)
                else:
                    print(f"La expresion a analizar da error: {self.line}")
                    error = "La expresion a analizar da error "
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)
            else:
                print(f"Error Intento de Contain en una variable no vectorial o Arreglo  linea:{self.line} ")
                error = "Error Intento de Contain en una variable no vectorial o Arreglo "
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)
        else:
            print(f"Error Contain en vector o Arreglo no declarado linea:{self.line} ")
            error = "Error Contain en vector o Arreglo no declarado linea "
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
        return self.value

    def getTipo(self, driver, ts):
        self.tipo=definirTipo(self.getValor(driver,ts))
        return self.tipo

    def generarC3d(self,ts:Enviroment,ptr):
        if self.falseLabel=="":
            self.falseLabel=self.generator.newLabel()
        if self.trueLabel=="":
            self.trueLabel=self.trueLabel
        # tpuntero = puntero
        # ttam= Heap[puntero]
        # puntero+=1
        # tcont=0
        # loop:
        #  if (tcont >= ttam) goto Lfalse
        #  	<instruccion Relacionales>
        #  Lv:
        #     goto Ltrue
        #  Lf:
        #     goto Loop
        result=ValC3d(valor="",isTemp=False,tipo=Tipos.ERROR,tipo_aux=Tipos.ERROR)
        self.generator.addComment(f"Contains Vector {self.id}")
        auxStack = self.generator.newTemp()
        symbol:Symbol = ts.buscarC3d(self.id,auxStack,self.en_funcion)
        if symbol != None:
            if symbol.tsimbolo == Symbols.VECTOR or symbol.tsimbolo == Symbols.ARREGLO:
                self.exp.generator = self.generator
                t_puntero = self.generator.newTemp()
                t_tam = self.generator.newTemp()
                t_valor = self.generator.newTemp()
                tcont = self.generator.newTemp()
                loop = self.generator.newLabel()
                lv = self.generator.newLabel()
                lf = self.generator.newLabel()
                self.generator.addBackStack(auxStack)
                auxIndex = self.generator.newTemp()
                self.generator.addExpression(target=auxIndex, left="P", right=str(symbol.position), operator="+")
                self.generator.addNextStack(auxStack)
                self.generator.addGetStack(target=t_puntero, index=auxIndex)
                if symbol.paso_parametro: #si fue declarado como paso de parametro en el anterior puntero esta la direccion del verdadero array
                                          # ubicado en el stack
                    self.generator.addGetStack(target=t_puntero, index=t_puntero)

                self.generator.addGetHeap(target=t_tam, index=t_puntero)  # t_tam=inicioArray
                self.generator.incVar(t_puntero)  # tpuntero=tpuntero+1
                if symbol.tsimbolo == Symbols.VECTOR:
                    #PARA PASAR DE LARGO EL CAPACITY
                    self.generator.incVar(t_puntero)# tpuntero=tpuntero+1
                self.generator.addExpAsign(target=tcont, right="0")  # tcont=0
                self.generator.addLabel(loop)#loop
                self.generator.addIf(left=tcont,rigth=t_tam,operator=">=",label=self.falseLabel)
                self.generator.addGetHeap(target=t_valor,index=t_puntero)
                self.generator.incVar(t_puntero)
                self.generator.incVar(tcont)
                #C3D DE LAS RELACIONALES
                expAux=AuxExp(valor=t_valor,tipo=symbol.tipo,tipoaux=symbol.tipo,line=symbol.line,column=symbol.column)
                C3dCmp=Relacionales(exp1=self.exp,operador="==",exp2=expAux,linea=self.line,columna=self.column)
                C3dCmp.generator=self.generator
                C3dCmp.trueLabel=lv
                C3dCmp.falseLabel=lf
                C3dCmp.generarC3d(ts,ptr)

                self.generator.addLabel(lv)
                self.generator.addGoto(self.trueLabel)
                self.generator.addLabel(lf)
                self.generator.addGoto(loop)

                result.tipo=Tipos.BOOLEAN
                result.tipo_aux=Tipos.BOOLEAN
                result.trueLabel=self.trueLabel
                result.falseLabel=self.falseLabel

            else:
                error = "Se intenta hacer push a una variable que no es un vector"
                print(error)

        else:
            error="No existe dicho arreglo"
            print(error)
        self.generator.addComment("END Contains")
        return result