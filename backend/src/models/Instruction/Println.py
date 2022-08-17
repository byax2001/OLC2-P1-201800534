from models.Instruction.Instruction import Instruccion
from models.Expresion.Expresion import Expresion
from models.Expresion.Primitivo import Primitivo
from models.TablaSymbols.Tipos import Tipos,Tipo
from models.TablaSymbols.Symbol import Symbols
from models.Expresion.Id import Id

class Println(Instruccion):

    def __init__(self, exp: Expresion,cExp:[Expresion], linea, columna):
        self.columna = columna
        self.linea = linea
        self.exp = exp
        self.cExp=cExp

    def ejecutar(self, driver, ts):
        if len(self.cExp)==0:
            if isinstance(self.exp,Primitivo):
                driver.append(str(self.exp.getValor(driver, ts))+"\n")
            else:
                print("Error: forma incorrecta de imprimir")
        else:
            #Conteo de {} y {:?} presentes en la variable auxiliar
            c_llaves=0   #llaves necesarias para imprimir
            c_llavesint=0  #para imprimir arrays enteros
            for element in self.cExp:
                if isinstance(element,Id):
                    Symbol=element.getSymbol(driver,ts)
                    if Symbol != None:
                        if Symbol.tsimbolo == Symbols.VARIABLE:
                            c_llaves+=1
                        elif Symbol.tsimbolo == Symbols.ARREGLO:
                            c_llavesint+=1
                        elif Symbol.tsimbolo == Symbols.FUNCION:
                            print("Se debe de ejecutar la funcion y no solo colocar id")
                            return
                    else:
                        print("Error una de las expresiones a imprimir es un id no declarado")
                        return
                else:
                    c_llaves+=1

            #reemplazo de los {} y {:?} por las expresiones en la cadena auxiliar, arriba se cubrieron todos los posibles errores, por lo cual no es necesario volver a cubrirlos
            #replace (exp1,exp2,1) indica que solo se reemplazara una vez de izquierda a derecha
            if self.exp.getTipo(driver,ts) == Tipos.STRING:
                v_exp=str(self.exp.getValor(driver,ts))
                if v_exp.count("{}")==c_llaves and v_exp.count("{:?}")==c_llavesint:
                    for exp in self.cExp: #se procede a recorrer cada expresion
                        valorCexp = str(exp.getValor(driver, ts))
                        if isinstance(exp, Id):  #si la expresion es un id, hay que analizar si es un arreglo o una variable
                            Symbol = element.getSymbol(driver, ts)
                            if Symbol.tsimbolo == Symbols.VARIABLE:
                                v_exp=v_exp.replace("{}",valorCexp,1)  #si es una variable normal se reemplaza de forma comun
                            elif Symbol.tsimbolo == Symbols.ARREGLO:
                                v_exp=v_exp.replace("{:?}",valorCexp,1) #si es un arreglo se reemplza {:?} por el arreglo
                        else:
                            v_exp=v_exp.replace("{}",valorCexp,1) #si es un primitivo u otro dato se reemplaza de forma comun
                    driver.append(v_exp+"\n") #se copia a la consola la cadena resultante
                else:
                    print("Error la expresion auxiliar no tiene la cantidad adecuada de {} y/o {:?}")
            else:
                print("Error la expresion auxiliar para imprimir variables no es string")