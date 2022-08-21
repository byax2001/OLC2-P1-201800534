from models.TablaSymbols.Tipos import Tipos
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
            self.vector.insert(index,valor)
            if self.stateCap == True:
                self.ocupado += 1
                if self.ocupado == self.capacity:
                    self.capacity = self.capacity * 2
        else:
            print("Error: ingreso de una posicion del vector fuera del rango")
    def remove(self,index:int):
        valor=self.vector.pop(index)
        if self.stateCap == True:
            self.ocupado -= 1
        return valor
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

    def Acces(self,indexs:[]):
        try:
            valor = self.vector
            for index in indexs:
                valor=valor[index]["valor"]
            return valor
        except:
            print("error, surgio un problema al acceder al contenido del vector")
            return None
