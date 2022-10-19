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
        init_code = len(self.generator.code)
        self.generator.addNextStack(index=str(ts.size))# P = P + oldTS_SIZE
        self.arreglo.generator=self.generator
        array:ValC3d = self.arreglo.generarC3d(ts,ptr)

        newts = Enviroment(ts,"ForIn")
        for_var = self.generator.newTemp()

        if array.prof_array == 0:
            symbol= Symbol(mut=True,id=self.id,value=for_var,tipo_simbolo=0,tipo=array.tipo,line=self.line,
                       column=self.column,tacceso=0,position=newts.size)
        else:
            nvector = VectorC3d(vec=array.valor, profundidad=array.prof_array)
            tsimbolo = 0
            if array.tipo_aux == Tipos.ARREGLO:
                tsimbolo=1
            elif array.tipo_aux == Tipos.VECTOR:
                tsimbolo=3
            symbol = Symbol(mut=True, id=self.id, value=nvector, tipo_simbolo=tsimbolo, tipo=array.tipo,
                            line=self.line, column=self.column, tacceso=0, position=newts.size)
        #SE DECLARA LA VARIABLE
        temp_var: SymC3d = newts.addVar(self.id, symbol)  # ----------------------------
        aux_index = self.generator.newTemp()  # tendra el index

        t_puntero = self.generator.newTemp()
        t_cont=self.generator.newTemp()
        t_tam=self.generator.newTemp()
        t_aux = self.generator.newTemp()
        loop = self.generator.newLabel()
        lsalida = self.generator.newLabel()


        self.generator.addExpAsign(target=t_puntero,right=array.valor)
        self.generator.addComment("Tcont")
        self.generator.addExpAsign(target=t_cont,right="-1")
        self.generator.addComment("tamanio")
        self.generator.addGetHeap(target=t_tam,index=t_puntero)
        self.generator.incVar(t_puntero)

        if array.tipo_aux == Tipos.VECTOR:
            self.generator.incVar(t_puntero)
        self.generator.addComment("Loop del For")
        self.generator.addLabel(loop) #LOOP:
        self.generator.incVar(t_cont)
        self.generator.addIf(left=t_cont,rigth=t_tam,operator=">=",label=lsalida)
        self.generator.addExpression(target=t_aux,left=t_puntero,right=t_cont,operator="+")
        self.generator.addGetHeap(target=for_var,index=t_aux) #tfor_v = Heap[tpuntero]
        # DECLARACION EN EL STACK
        self.generator.addExpression(target=aux_index, left="P", right=str(temp_var.position), operator="+")
        self.generator.addSetStack(index=aux_index, value=for_var)  # Stack[(int)pos]= val

        self.generator.addComment("Instrucciones For")
        for ins in self.cInst:
            ins.generator=self.generator
            ins.generarC3d(newts,ptr)

        self.generator.addGoto(loop) #Goto Loop
        self.generator.addLabel(lsalida) #Lsalida:

        self.generator.addBackStack(index=str(ts.size))# P = P - oldTS_SIZE
        f_code = len(self.generator.code)
        code = ""
        for x in range(init_code, f_code):
            if x != f_code - 1:
                code += self.generator.code[x] + "\n"
            else:
                code += self.generator.code[x]
        for x in reversed(range(init_code, f_code)):
            self.generator.code.pop(x)
        code = code.replace("break_i", f"goto {lsalida};")
        code = code.replace("continue_i", f"goto {loop};")
        self.generator.addCode(code)