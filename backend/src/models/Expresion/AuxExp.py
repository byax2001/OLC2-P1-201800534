from models.Abstract.Expresion import Expresion
from models.TablaSymbols.ValC3d import ValC3d
class AuxExp(Expresion):
    def __init__(self,valor,tipo,tipoaux,line,column):
        super().__init__()
        self.prof_array=0
        self.valor=valor
        self.tipo=tipo
        self.tipoaux=tipoaux
        self.line=line
        self.column=column
    def generarC3d(self,ts,ptr):
        tmpR=self.generator.newTemp()
        self.generator.addExpAsign(target=tmpR,right=self.valor)
        result=ValC3d(valor=tmpR,isTemp=True,tipo=self.tipo,tipo_aux=self.tipoaux)
        result.prof_array=self.prof_array
        return result