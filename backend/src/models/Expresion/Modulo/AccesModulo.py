from models.Expresion.Expresion import Expresion
from models.TablaSymbols.Enviroment import Enviroment
from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Symbol import Accesos
from models.Instruction.Call import Call
from BaseDatos.B_datos import B_datos

from models.TablaSymbols.Symbol import Symbols
class AccesModulo(Expresion):
    def __init__(self,id,cIds:[str],Parametros:[Expresion],line:int,column:int):
        self.value=None
        self.tipo=None
        self.id=id
        self.cId=cIds
        self.params=Parametros
        self.line=line
        self.column=column
        self.instancia=0
    def getValor(self, driver, ts:Enviroment):
        self.instancia += 1
        if self.value==None and self.tipo==None:
            modulo=ts.buscar(self.id)
            if modulo!=None:
                if modulo.tipo==Tipos.MODULO:
                    v_mod=modulo.value
                    v_mod.tabla.update(ts.tabla)  #el contenido de los enviroments mod deben de ser actualizados con el enviroment
                                                  #principal cada vez que se usan pues estos no se actualian automaticamente
                                                  #como si lo hace el enviroment principal
                    for x in range(len(self.cId)-1): #se recorre hasta llegar el penultimo id
                        v_mod=v_mod.buscar(self.cId[x])
                        if v_mod!=None:
                            if v_mod.tipo==Tipos.MODULO or v_mod.tipo==Tipos.STRUCT:
                                v_mod=v_mod.value
                            else:
                                error = "La variable no posee dichos componentes"
                                print(error)
                                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                                  columna=self.column)
                        else:

                            error="Error: La variable no posee dichos componentes"
                            print(error)
                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                              columna=self.column)
                    element=v_mod.buscar(self.cId[len(self.cId)-1])
                    if element !=None:
                        if element.tacceso!=Accesos.PRIVADO:
                            if element.tsimbolo == Symbols.FUNCION:
                                callf=Call(id=self.cId[len(self.cId)-1],cExp=self.params,line=self.line,column=self.column)
                                self.tipo = callf.getTipo(driver, v_mod)
                                self.value=callf.getValor(driver,v_mod)
                            else:
                                error="element de mod no es funcion "
                                print(error)
                                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                                  columna=self.column)
                        else:
                            error = "Error no se puede acceder al elemento pues es privado"
                            print(error)
                            B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                              columna=self.column)
                    else:
                        error = "Error el modulo o submodulo no cuenta con dicho parametro "
                        print(error)
                        B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                          columna=self.column)
                else:
                    error = "la variable a la que se desea acceder como modulo no lo es"
                    print(error)
                    B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                      columna=self.column)

            else:
                error = "El modulo no ha sido declarado"
                print(error)
                B_datos().appendE(descripcion=error, ambito=ts.env, linea=self.line,
                                  columna=self.column)

        return self.value

    def getTipo(self, driver, ts):
        self.resetInst()
        if self.tipo == None:
            self.getValor(driver, ts)
            if self.value == None:
                self.tipo == Tipos.ERROR
        else:
            self.instancia+=1
        return self.tipo
    def ejecutar(self,driver,ts):
        self.getTipo(driver,ts)
        self.getValor(driver,ts)

    def resetInst(self):
        if self.instancia>1:
            self.instancia=0
            self.value=None
            self.tipo=None