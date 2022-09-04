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
    

#Lista de errores
@app.route("/lerrores",methods=["GET","POST"])
def ListaErrores():
    JsonF={"Contenido":B_datos().rLerrores()}
    return JsonF

#Lista de tabla de simbolos
@app.route("/ltsimbolos",methods=["GET","POST"])
def ListaTsimbolos():
    JsonF={"Contenido":B_datos().rLTsimbolos()}
    return JsonF

#lista de Base de datos
@app.route("/lbdatos",methods=["GET","POST"])
def ListaBaseDatos():
    JsonF={"Contenido":B_datos().rLB_datos()}
    return JsonF

#lista de tabla de base de datos
@app.route("/lt_bdatos",methods=["GET","POST"])
def ListaTablaBaseDatos():
    JsonF={"Contenido":B_datos().rL_tBdatos()}
    return JsonF




if __name__=="__main__":
    app.run(debug=True)