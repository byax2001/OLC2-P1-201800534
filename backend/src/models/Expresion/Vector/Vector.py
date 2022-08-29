from models.TablaSymbols.Tipos import Tipos
from models.TablaSymbols.Enviroment import Enviroment
class Vector:
    def __init__(self,vec,stateCap,capacity):
        self.vector=vec
        self.stateCap=stateCap #si es false no es necesario verificar si el vector esta lleno o no
        self.capacity=capacity
        self.ocupado=0
    def push(self,valor):
        self.vector.append(valor)
        if self.stateCap==True:
            self.ocupado+=1
            if self.ocupado==self.capacity:
                self.capacity=self.capacity*2
    def insert(self,index:int,valor):
        if index<len(self.vector):
            #colocar que el seguro de que index debe de ser TIPO.INT64
            self.vector.insert(index,valor)
            if self.stateCap == True:
                self.ocupado += 1
                if self.ocupado == self.capacity:
                    self.capacity = self.capacity * 2
        else:
            print("Error: ingreso de una posicion del vector fuera del rango")
    def remove(self,index:int):
        if index<len(self.vector):
            valor=self.vector.pop(index)["valor"]

            if self.stateCap == True:
                self.ocupado -= 1
            return valor
        else:
            print("Error: posicion a remover fuera del rango del vector")
    def contains(self,valor):
        for element in self.vector:
            if element["valor"]==valor:
                return True
        return False
    def len(self):
        return len(self.vector)

    def rcapacity(self):
        if self.stateCap==False:
            self.capacity=len(self.vector)+1
        return self.capacity

    def acces(self,cIndex:[]):
        try: #Try como precaucion en caso se intente ingresar a una posicion de memoria fuera del rango del vector
            valor = self.vector
            for index in cIndex:
                valor=valor[index]["valor"]
            return valor
        except:
            print("error, surgio un problema al acceder al contenido del vector")
            return None
    def updateVector(self,cIndex:[],valor):
        try: #Try como precaucion en caso se intente ingresar a una posicion de memoria fuera del rango del vector
            vector = self.vector
            x=0
            for index in cIndex:
                x+=1
                if x==len(cIndex):
                    vector[index]["valor"]=valor
                    return True
                vector=vector[index]["valor"]

            return False
        except:
            print("error, surgio un problema al asignar un valor al contenido del vector o arreglo")
            return False

    def updateVectorStruct(self, cIndex: [],cIds:[], valor,tipo_val):
        try:  # Try como precaucion en caso se intente ingresar a una posicion de memoria fuera del rango del vector
            vector = self.vector
            x = 0
            tipo=Tipos.ERROR
            for index in cIndex:
                tipo = vector[index]["tipo"]
                vector = vector[index]["valor"]

            if tipo==Tipos.STRUCT:
                nodo:Enviroment=vector
                x=0

                for id in cIds:
                    nodo=nodo.buscar(id);
                    x+=1
                    if nodo.tipo!=Tipos.STRUCT and x!=len(cIndex):
                        print("Error la variable no cuenta con tantos parametros anidados")
                        return

                if tipo_val==nodo.tipo:
                    nodo.value=valor
                else:
                    print("Error los tipos del paramatero de la variable struct y el nuevo valor no son los mismos")
            else:
                print("Error el elemento no es una variable objeto que tenga el resto de parametros indicados")
        except Exception as e:
            print(e)
            print("error, surgio un problema al asignar un valor al contenido del vector o arreglo")
            return False
