from gramatica.parser import parser
from models.TablaSymbols.Enviroment import Enviroment
from models.Driver import Driver
from models.Ast.Ast import Ast


f = open("./entrada.txt", "r")
input = f.read()
print(input)

ast: Ast =parser.parse(input)
ts = Enviroment(None, 'Global')
driver = Driver()

ast.ejecutar(driver, ts)

print(driver.console)