from flask import Flask,request
import json
from flask_cors import  CORS,cross_origin

app=Flask(__name__)
cors=CORS(app)
app.config['CORS_HEADERS']="Content-Type"


#ENVIA UN JSON
@app.route("/lfechas",methods=["GET","POST"])
def LAnalizar():
    if request.method == "GET":
        jsonE = json.loads(request.data)
        Lf="hola"
        JsonF={"Contenido":Lf}
        return JsonF
#Prueba
@app.route("/", methods=["GET","POST"])
def prueba():
    return f"Hola "
    
@app.route("/", methods=["GET","POST"])   
def prueba1():
    if request.method == "POST":
        l = request.data
        return f"Hola "

if __name__=="__main__":
    app.run(debug=True)