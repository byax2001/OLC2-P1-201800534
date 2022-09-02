from models.Instruction.Instruction import Instruccion
from models.Expresion.Expresion import Expresion
from models.Expresion.Primitivo import Primitivo
from models.TablaSymbols.Tipos import Tipos,Tipo
from models.TablaSymbols.Symbol import Symbols
from models.Expresion.Id import Id
#VECTORES Y ARRAYS
from models.Expresion.Vector.vecI import vecI
from models.Expresion.Arreglo.Arreglo import Arreglo

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
                    Symbol=element.getSymbol(driver,ts) #este metodo se encuentra declarado en la clase Id.py
                    if Symbol != None:
                        if Symbol.tsimbolo == Symbols.VARIABLE:
                            c_llaves+=1
                        elif Symbol.tsimbolo == Symbols.ARREGLO or Symbol.tsimbolo == Symbols.VECTOR:
                            c_llavesint+=1
                        elif Symbol.tsimbolo == Symbols.FUNCION:
                            print("Se debe de ejecutar la funcion y no solo colocar id")
                            return
                    else:
                        print("Error una de las expresiones a imprimir es un id no declarado")
                        return
                elif isinstance(element,vecI) or isinstance(element,Arreglo):
                    c_llavesint+=1;
                elif isinstance(element,Primitivo):
                    c_llaves+=1

            #reemplazo de los {} y {:?} por las expresiones en la cadena auxiliar, arriba se cubrieron todos los posibles errores, por lo cual no es necesario volver a cubrirlos
            #replace (exp1,exp2,1) indica que solo se reemplazara una vez de izquierda a derecha
            if self.exp.getTipo(driver,ts) == Tipos.STR: #<--------expresion auxiliar "{}  {:?}"
                v_exp=str(self.exp.getValor(driver,ts))
                if v_exp.count("{}")==c_llaves and v_exp.count("{:?}")==c_llavesint:
                    for exp in self.cExp: #se procede a recorrer cada expresion
                        valorCexp = exp.getValor(driver, ts)
                        t_valorCexp=exp.getTipo(driver,ts)
                                    #el getvalor de un id que es vector o arreglo devuelve el vector contenido en la clase VECTOR por un metodo en la clase ID.py
                        if isinstance(exp, Id):  #si la expresion es un id, hay que analizar si es un arreglo o una variable
                            Symbol = exp.getSymbol(driver, ts)
                            if Symbol.tsimbolo == Symbols.VARIABLE:
                                v_exp=v_exp.replace("{}",str(valorCexp),1)  #si es una variable normal se reemplaza de forma comun
                            elif Symbol.tsimbolo == Symbols.ARREGLO or Symbol.tsimbolo == Symbols.VECTOR:
                                valorCexp=self.printArray(valorCexp); #metodo para imprimir un array correctamente
                                v_exp=v_exp.replace("{:?}",valorCexp,1) #si es un arreglo se reemplza {:?} por el arreglo
                        elif type(valorCexp)==list: #si el valor a imprimir es un array
                            valorCexp = self.printArray(valorCexp)
                            v_exp = v_exp.replace("{:?}", valorCexp, 1)
                        else:
                            v_exp=v_exp.replace("{}",str(valorCexp),1) #si es un primitivo u otro dato se reemplaza de forma comun
                    driver.append(v_exp+"\n") #se copia a la consola la cadena resultante
                else:
                    print("---------------------------------PRINT-------------------------------")
                    for element in self.cExp:

                        tipo = element.getTipo(driver, ts)
                        valor = element.getValor(driver, ts)
                        if type(valor) == list:
                            valor=self.printArray(valor)
                            v_exp = v_exp.replace("{:?}", str(valor), 1)
                        else:
                            v_exp = v_exp.replace("{}", str(valor), 1)
                    if v_exp.count("{}")==0 and v_exp.count("{:?}")==0:
                        driver.append(str(v_exp) + "\n")
                    else:
                        print("Error la expresion auxiliar no tiene la cantidad adecuada de {} y/o {:?}")
            else:
                print("Error la expresion auxiliar para imprimir variables no es string")

    def printArray(self,arrayVec):
        vector="["
        if type(arrayVec)==list:
            for x in range(len(arrayVec)):
                v_element = arrayVec[x]["valor"]
                if type(v_element)==list:
                    v_element=self.printArray(v_element)
                if x!=(len(arrayVec)-1):
                    vector=vector+str(v_element)+","
                else:
                    vector=vector+str(v_element)+"]"
            if len(arrayVec)==0:
                vector=vector+"]"
        return vector