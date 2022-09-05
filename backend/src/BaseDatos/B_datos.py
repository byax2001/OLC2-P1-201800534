from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Symbol import Symbols
import time

class B_datos(object):
    instance=None
    prueba=[]
    Lerrores=[]
    Lts=[]
    LBase_datos=[]
    Ltablas_Bdatos=[]

    def __new__(cls):
        if B_datos.instance==None:
            B_datos.instance=object.__new__(cls)
        return B_datos.instance

    def clearListas(self):
        B_datos.Lerrores=[]
        B_datos.Lvar=[]
        B_datos.LBase_datos=[]
        B_datos.Ltablas_Bdatos=[]

    def appendVar(self,id,t_simbolo,t_dato,ambito,fila,columna):
        if ambito!="Global":
            ambito="Local"
        t_simbolo=B_datos.tipoVar(t_simbolo)
        t_dato=B_datos.tipoDato(t_dato)
        variable={"nombre":id,"tiposimbolo":t_simbolo,"tipodato":t_dato,"ambito":ambito,"fila":fila,"columna":columna}
        B_datos.Lts.append(variable)

    def appendE(self,descripcion,ambito,linea,columna):
        if ambito!="Global":
            ambito="Local"
        nerror=len(B_datos.Lerrores)
        tiempo=str(time.strftime("%d/%m/%y"))+" "+str(time.strftime("%I:%M"))
        error={"No":nerror,"descripcion":descripcion,"ambito":ambito,"linea":linea,"columna":columna,"tiempo":tiempo}
        B_datos.Lerrores.append(error)

    def appendBdatos(self,id:str,ntablasC,linea:int):
        nBdatos = len(B_datos.LBase_datos)
        tabla_bdatos={"No":nBdatos,"nombre":id,"ntablas":ntablasC,"linea":linea}
        B_datos.LBase_datos.append(tabla_bdatos)

    def appendT_bdatos(self,id,BdatosSuperior,linea:int):
        ntablas = len(B_datos.Ltablas_Bdatos)
        T_bdatos={"No":ntablas,"nombre":id,"nameBd":BdatosSuperior,"linea":linea}
        B_datos.Ltablas_Bdatos.append(T_bdatos)

    def rtime(self):
        return str(time.strftime("%d/%m/%y"))+" "+str(time.strftime("%I:%M"))

    def rLerrores(self):
        return B_datos.Lerrores

    def rLTsimbolos(self):
        return B_datos.Lts

    def rLB_datos(self):
        return B_datos.LBase_datos

    def rL_tBdatos(self):
        return B_datos.Ltablas_Bdatos

    def tipoVar(tipo:Tipos):
        stipo = ""
        if tipo== Symbols.VARIABLE:
            stipo="variable"
        elif tipo==  Symbols.ARREGLO:
            stipo = "arreglo"
        elif tipo==  Symbols.FUNCION:
            stipo = "funcion"
        elif tipo==  Symbols.VECTOR:
            stipo = "vector"
        elif tipo==  Symbols.OBJETO:
            stipo = "objeto"
        elif tipo==  Symbols.MOD:
            stipo = "modulo"
        return stipo

    def tipoDato(tipo:Symbols):
        stipo=""
        if tipo==Tipos.INT64:
            stipo="i64"
        elif tipo==Tipos.FLOAT64:
            stipo = "f64"
        elif tipo==Tipos.STRING:
            stipo = "String"
        elif tipo==Tipos.STR:
            stipo = "str"
        elif tipo==Tipos.CHAR:
            stipo = "char"
        elif tipo==Tipos.BOOLEAN:
            stipo = "bool"
        elif tipo==Tipos.ERROR:
            stipo = "error"
        elif tipo==Tipos.ID:
            stipo = "id"
        elif tipo==Tipos.VOID:
            stipo = "void"
        elif tipo==Tipos.USIZE:
            stipo = "usize"
        elif tipo==Tipos.STRUCT:
            stipo = "struct"
        elif tipo==Tipos.MODULO:
            stipo = "modulo"
        elif tipo==Tipos.ARREGLO:
            stipo = "arreglo"
        return  stipo



