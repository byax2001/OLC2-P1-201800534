from flask import Flask,request
import json
from flask_cors import  CORS,cross_origin
from models.TablaSymbols.Enviroment import Enviroment
from models.Driver import Driver
from models.Ast.Ast import Ast
from models.Instruction.Call import Call
from BaseDatos.B_datos import B_datos
from gramatica.parser import parser
from models.Expresion.Nothing import Nothing
from models.TablaSymbols.Symbol import Symbols
from Generator3D.Generator3D import Generator
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
        if ast==None:
            ast=Nothing(line=0,column=0)

        ast.ejecutar(driver, ts)
        main = ts.buscar("main")
        if main != None:  #debe de existir obligatoriamente una funcion main
            call = Call("main", [], line=0, column=0);
            call.ejecutar(driver, ts)
            #verificar que existan modulos
            nModulos=0
            elGlobal=ts.tabla
            for element in elGlobal:
                symbol=elGlobal[element]
                if symbol.tsimbolo == Symbols.MOD:
                    nHijos=moduloshijos(symbol)
                    B_datos().appendBdatos(id=symbol.id,ntablasC=nHijos,linea=symbol.line)
                    nModulos+=1
            if nModulos==0:
                B_datos().appendE(descripcion="No hay modulos en el archivo",ambito="Global",linea=0,columna=0)

        else:
            print("Error no existe main en el archivo")

        print("driver cnsASDF-----------------------------------")
        print(driver.console)
        print(B_datos().rLerrores())
        JsonF={"Contenido":driver.console}
    return JsonF


@app.route("/DataAnalisisC3d",methods=["GET","POST"])
def DataAnalisisC3d():
    B_datos().clearListas()  # se limpian todas las listas a la hora de analizar
    if request.method == "POST":
        jsonR = json.loads(request.data)
        input = jsonR[0]["entrada"]
        ast: Ast = parser.parse(input)
        ts = Enviroment(None, 'Global')
        generator: Generator = Generator()
        if ast == None:
            ast = Nothing(line=0, column=0)
            ast.generarC3d(ts=ts, ptr=0)
        else:
            ast.generarC3d(ts=ts, generator=generator)
        main = ts.buscar("main")
        if main != None:
            call = Call("main", [], line=0, column=0);
            # call.ejecutar(driver,ts)
            call.generator = generator
            call.generarC3d(ts=ts, ptr=0)
            #PARA REGISTRAR EL ERROR DE QUE NO HAY MODULOS EN LOS ARCHIVOS
            nModulos = 0
            elGlobal = ts.tabla
            for element in elGlobal:
                symbol = elGlobal[element]
                if symbol.tsimbolo == Symbols.MOD:
                    nHijos = moduloshijos(symbol)
                    B_datos().appendBdatos(id=symbol.id, ntablasC=nHijos, linea=symbol.line)
                    nModulos += 1
            if nModulos == 0:
                B_datos().appendE(descripcion="No hay modulos en el archivo", ambito="Global", linea=0, columna=0)
        else:
            print("Error no existe main en el archivo")
        c3d = generator.getCode()
        print("\n CODIGO 3D: ")
        print(c3d)
        JsonF = {"Contenido": c3d}
    return JsonF

def moduloshijos(symbol):
    nmodH=0
    symval=symbol.value
    envMod=symval.tabla
    for element in envMod:
        symbolsub = envMod[element]
        if symbolsub.tsimbolo == Symbols.MOD:
            B_datos().appendT_bdatos(id=symbolsub.id,BdatosSuperior=symbol.id,linea=symbolsub.line)
            nmodH+=1
    return nmodH

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