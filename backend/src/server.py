from flask import Flask,request
import json
from flask_cors import  CORS,cross_origin
from models.TablaSymbols.Enviroment import Enviroment
from models.Driver import Driver
from models.Ast.Ast import Ast
from models.Instruction.Call import Call
from BaseDatos.B_datos import B_datos
from gramatica.parser import parser

app=Flask(__name__)
cors=CORS(app)
app.config['CORS_HEADERS']="Content-Type"

#RECIBE LOS EVENTOS
#Reventos: recibir eventos
@app.route("/DataAnalisis",methods=["GET","POST"])
def DataAnalisis():
    B_datos().clearListas() #se limpian todas las listas a la hora de analizar
    if request.method == "POST":
        jsonR=json.loads(request.data)
        input=jsonR[0]["entrada"]
        ast: Ast = parser.parse(input)
        ts = Enviroment(None, 'Global')
        driver = Driver()

        ast.ejecutar(driver, ts)
        main = ts.buscar("main")
        if main != None:
            call = Call("main", [], line=0, column=0);
            call.ejecutar(driver, ts)
        else:
            print("Error no existe main en el archivo")
        JsonF={"Contenido":driver.console}
    return JsonF
    

#ENVIA UN JSON
@app.route("/lfechas",methods=["GET","POST"])
def Lfechas():
    jsonE = json.loads(request.data)
    JsonF={"Contenido":3}
    return JsonF

@app.route("/",methods=["GET","POST"])
def prueba():
    if request.method == "POST":
        l = json.loads(request.data)
        print(l)
        x=l[0]["entrada"]
        print("AAAAAAAAAAAAAAAAAAAAAAA")
        print(x)
        JsonF={"Contenido":3}
    return JsonF



if __name__=="__main__":
    app.run(debug=True)