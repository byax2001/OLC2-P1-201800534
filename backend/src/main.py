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


ast: Ast =parser.parse(input)
ts = Enviroment(None, 'Global')
ts_c3d = Enviroment(None, 'Global')
driver = Driver()
generator: Generator = Generator()

ast.ejecutar(driver, ts)
ast.generarC3d(ts=ts_c3d,generator= generator)
main=ts.buscar("main")
if main!=None:
    call=Call("main",[],line=0,column=0);
    #call.ejecutar(driver,ts)
    call.generator=generator
    call.generarC3d(ts=ts_c3d,ptr=0)
else:
    print("Error no existe main en el archivo")
print("OUTPUT:")
print(driver.console)
print("\n CODIGO 3D: ")
print(generator.getCode())
#salida
f2 = open("./salida.txt","w")
f2.write(generator.getCode())
#Generator.getCode() para obtener el string de lo generado