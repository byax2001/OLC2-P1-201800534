
from gramatica.parser import parser

f = open("./entrada.txt", "r")
input = f.read()
print(input)
result=parser.parse(input)
print(result)