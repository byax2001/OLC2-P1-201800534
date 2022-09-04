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

