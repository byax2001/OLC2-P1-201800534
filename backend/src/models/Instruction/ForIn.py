#0..4 arreglo del 0 al  4 [1,2,3,4]
#"hola".char() arreglo ['h','o','l','a']
# array o vector
from models.Abstract.Instruction import Instruccion
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.Symbol import Symbol,Symbols
from models.Driver import Driver
from models.Instruction.Break import Break
from models.Instruction.Return import Return
from models.Instruction.Continue import Continue
from BaseDatos.B_datos import B_datos
from models.TablaSymbols.ValC3d import ValC3d
from models.TablaSymbols.Tipos import Tipos
from models.Expresion.Vector.VectorC3d import VectorC3d
from models.TablaSymbols.SymC3d import SymC3d

class ForIn(Instruccion):
    def __init__(self,id:str,arreglo,cInst:[Instruccion],line:int,column:int):
        super().__init__()
        self.id=id
        self.arreglo=arreglo
        self.cInst=cInst
        self.line=line
        self.column=column
    def ejecutar(self, driver: Driver, ts: Enviroment):
        new_ts=Enviroment(ts,"ForIn")

        tArr=self.arreglo.getTipo(driver,ts)
        cArr = self.arreglo.getValor(driver, ts)
        if type(cArr)==list:
            symbol=Symbol(mut=True,id=self.id,value="",tipo_simbolo=0,tipo=tArr,line=self.line,column=self.column)
            new_ts.addVar(self.id,symbol)
            for element in cArr:
                new_ts.updateForIn(self.id, element["valor"])  # actualizar variable id en cada iteracion
                new_ts2 = Enviroment(new_ts, "Bloque ForIn")
                for inst in self.cInst:
                    if isinstance(inst,Break):
                        return
                    elif isinstance(inst,Continue):
                        break
                    elif isinstance(inst,Break):
                        print("Error hay un return en un for")
                        error = "Error hay un return en un for"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                          columna=self.column)
                        return
                    rInst=inst.ejecutar(driver,new_ts2)

                    if isinstance(rInst, Break):
                        return
                    elif isinstance(rInst, Continue):
                        break
                    elif isinstance(rInst, Return):
                        print("Error, existe return afuera de una funcion")
                        error = "Error, existe return afuera de una funcion"
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                          columna=self.column)
                        return
        else:
            print("Error intento de for in en un elemento que no es arreglo o rango")
            error = "Error intento de for in en un elemento que no es arreglo o rango"
            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                              columna=self.column)
    def generarC3d(self,ts:Enviroment,ptr):
        self.generator.addComment("FOR IN")
        self.generator.addNextStack(index=str(ts.size))# P = P + oldTS_SIZE
        self.arreglo.generator=self.generator
        array:ValC3d = self.arreglo.generarC3d(ts,ptr)

        newts = Enviroment(ts,"ForIn")
        for_var = self.generator.newTemp()
        if array.prof_array == 1:
            symbol= Symbol(mut=True,id=self.id,value=for_var,tipo_simbolo=0,tipo=array.tipo,line=self.line,
                       column=self.column,tacceso=0,position=newts.size)
        else:
            nvector = VectorC3d(vec=array.valor, profundidad=(array.prof_array + 1))
            tsimbolo = 0
            if array.tipo_aux == Tipos.ARREGLO:
                tsimbolo=1
            elif array.tipo_aux == Tipos.VECTOR:
                tsimbolo=3
            symbol = Symbol(mut=True, id=self.id, value=nvector, tipo_simbolo=tsimbolo, tipo=array.tipo,
                            line=self.line, column=self.column, tacceso=0, position=newts.size)
        newts.addVar(id=self.id,simbolo=symbol)
        temp_var: SymC3d = ts.addVar(self.id, symbol)  # ----------------------------
        aux_index = self.generator.newTemp()  # tendra el index
        #DECLARACION EN EL STACK
        self.generator.addExpression(target=aux_index, left="P", right=str(temp_var.position), operator="+")
        self.generator.addSetStack(index=aux_index, value=str(temp_var.valor))  # Stack[(int)pos]= val

        t_puntero = self.generator.newTemp()
        t_cont=self.generator.newTemp()
        t_tam=self.generator.newTemp()
        loop = self.generator.newLabel()
        lsalida = self.generator.newLabel()

        self.generator.addExpAsign(target=t_puntero,right=array.valor)
        self.generator.addComment("Tcont")
        self.generator.addExpAsign(target=t_cont,right="0")
        self.generator.addComment("tamanio")
        self.generator.addGetHeap(target=t_tam,index=t_puntero)
        self.generator.incVar(t_puntero)
        if array.tipo_aux == Tipos.VECTOR:
            self.generator.incVar(t_puntero)


        self.generator.addBackStack(index=ts.size)# P = P - oldTS_SIZE
