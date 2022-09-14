from gramatica.parser import parser
from models.TablaSymbols.Enviroment import Enviroment
from models.Driver import Driver
from models.Ast.Ast import Ast
from models.Instruction.Call import Call
from BaseDatos.B_datos import B_datos
from Generator3D.Generator3D import Generator

B_datos()
l=B_datos()

f = open("./entrada.txt", "r")
input = f.read()
print(input)

ast: Ast =parser.parse(input)
ts = Enviroment(None, 'Global')
driver = Driver()
generator: Generator = Generator()

ast.ejecutar(driver, ts, generator)

main=ts.buscar("main")
if main!=None:
    call=Call("main",[],line=0,column=0);
    call.ejecutar(driver,ts)
else:
    print("Error no existe main en el archivo")
print("OUTPUT:")
print(driver.console)
print("\n CODIGO 3D: ")
print(generator.getCode())
#Generator.getCode() para obtener el string de lo generado