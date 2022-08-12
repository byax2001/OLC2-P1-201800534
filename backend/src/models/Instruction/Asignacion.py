from models.Instruction.Instruction import Instruccion
from models.Expresion.Expresion import Expresion

class Asignacion(Instruccion):
    def __init__(self,id:str, exp: Expresion, linea:int, columna:int):
        self.id=id
        self.exp = exp
        self.linea = linea
        self.columna = columna

    def ejecutar(self, driver, ts):
        Symbol=ts.buscar(self.id);
        if Symbol !=None:
            if(Symbol.mut==True):
                v_exp=self.exp.getValor(driver,ts)
                if(v_exp!=None):
                    t_exp=self.exp.getTipo(driver,ts)
                    if Symbol.tipo == t_exp:
                        ts.actualizar(self.id,v_exp);
                    else:
                        print("El valor a asignar es de distinto tipo al de la variable")
                else:
                    print("El valor que se intenta asignar a la variable es None o da error")
            else:
                print("La variable que intenta cambiar no es muteable")
        else:
            print("No ha sido declarada dicha variable")