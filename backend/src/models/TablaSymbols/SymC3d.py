class SymC3d:
    #Nuestros simbolos poseen un id, un valor y un tipo
    def __init__(self, id: str, type, position):
        self.id = id
        self.tipo = type
        self.position = position

    def getId(self):
        return self.id

    def getValue(self):
        return self.value

    def getType(self):
        return self.type
