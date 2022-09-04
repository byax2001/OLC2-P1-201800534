from gramatica.parser import parser
from models.TablaSymbols.Enviroment import Enviroment
from models.Driver import Driver
from models.Ast.Ast import Ast
from models.Instruction.Call import Call
from BaseDatos.B_datos import B_datos


B_datos()
l=B_datos()

f = open("./entrada.txt", "r")
input = f.read()
print(input)

ast: Ast =parser.parse(input)
ts = Enviroment(None, 'Global')
driver = Driver()

ast.ejecutar(driver, ts)
main=ts.buscar("main")
if main!=None:
    call=Call("main",[],line=0,column=0);
    call.ejecutar(driver,ts)
else:
    print("Error no existe main en el archivo")
print("OUTPUT:")
print(driver.console)
