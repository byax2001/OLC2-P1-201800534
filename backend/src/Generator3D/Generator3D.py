class Generator:
    def __init__(self) -> None:
        self.generator = None
        self.temporal = 0
        self.label = 0
        self.code = []
        self.tempList = []

    # Obtener los temporales usados y que estan en un alista unidos y separados por comas
    def getUsedTemps(self) -> str:
        return ",".join(self.tempList)

    # Obtener el codigo generado
    def getCode(self) -> str:
        tempCode: str = '#include <stdio.h>\n'
        tempCode = tempCode + '#include <math.h>\n'
        tempCode = tempCode + "double HEAP[10000];\n"
        tempCode = tempCode + "double STACK[78000];\n"
        tempCode = tempCode + "double P;\n"  #p, h y ptr se inicializan con 0 en c++ si no se les asigna nada al declararlos
        tempCode = tempCode + "double H;\n"
        tempCode = tempCode + "double ptr;\n"

        if (len(self.tempList) > 0):
            tempCode = tempCode + "double " + self.getUsedTemps() + ";\n\n"

        tempCode = tempCode + '\nint main(){\n'
        tempCode = tempCode + "\n".join(self.code)
        tempCode = tempCode + '\nreturn 0;\n}\n'

        return tempCode

    # Generar un nuevo temporal
    def newTemp(self) -> str:
        temp = "t" + str(self.temporal)
        self.temporal = self.temporal + 1

        # Lo guardamos para declararlo
        self.tempList.append(temp)
        return temp

    # Generador de label
    def newLabel(self) -> str:
        temp = self.label
        self.label = self.label + 1
        return "L" + str(temp)

    def addCallFunc(self, name: str):
        self.code.append(name + "();")

    # Añade label al codigo
    def addLabel(self, label: str):
        self.code.append(label + ":")

    def addExpression(self, target: str, left: str, right: str, operator: str):
        self.code.append(target + " = " + left + " " + operator + " " + right + ";")

    def addIf(self, left: str, rigth: str, operator: str, label: str):
        self.code.append("if(" + left + " " + operator + " " + rigth + ") goto " + label + ";")

    def addGoto(self, label: str):
        self.code.append("goto " + label + ";")

    # Añade un printf
    def addPrintf(self, typePrint: str, value: str):
        self.code.append("printf(\"%" + typePrint + "\"," + value + ");")

    # Salto de linea
    def addNewLine(self):
        self.code.append('printf(\"%c\",10);')

    # Se mueve hacia la posicion siguiente del heap
    def addNextHeap(self):
        self.code.append("H = H + 1;")

    # Se mueve hacia la posicion siguiente del stack
    def addNextStack(self, index: str):
        self.code.append("P = P + " + index + ";")

    # Se mueve hacia la posicion anterior del stack
    def addBackStack(self, index: str):
        self.code.append("P = P - " + index + ";")

    # Obtiene el valor del heap en cierta posicion
    def addGetHeap(self, target: str, index: str):
        self.code.append(target + " = HEAP[(int)" + index + " ];")

    # Inserta valor en el heap
    def addSetHeap(self, index: str, value: str):
        self.code.append("HEAP[(int)" + index + "] = " + value + ";")

    # Obtiene valor del stack en cierta posicion
    def addGetStack(self, target: str, index: str):
        self.code.append(target + " = STACK[(int)" + index + "];")

    # INserta valor al stack
    def addSetStack(self, index: str, value: str):
        self.code.append("STACK[(int)" + index + "] = " + value + ";")

    def addptr(self,valor,ope):
        self.addExpression("ptr","ptr",valor,ope)

    def addError(self,error:str):
        for char in error:
            self.addPrintf("c",str(ord(char)))
    def addComment(self,comment:str):
        self.code.append(f"/* {comment} */")






