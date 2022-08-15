from models.Instruction.Instruction import Instruccion
from models.Expresion.Expresion import Expresion
from models.Expresion.Primitivo import Primitivo

class Println(Instruccion):

    def __init__(self, exp: Expresion, linea, columna):
        self.columna = columna
        self.linea = linea
        self.exp = exp

    def ejecutar(self, driver, ts):
        driver.append(str(self.exp.getValor(driver, ts))+"\n")