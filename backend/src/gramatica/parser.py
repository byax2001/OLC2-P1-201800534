from ply.yacc import yacc
from gramatica import lexer
from models.Ast.Ast import Ast
#Expresiones
from models.Expresion.Operacion.Aritmeticas import Aritmeticas
from models.Expresion.Operacion.Relacionales import Relacionales
from models.Expresion.Operacion.Logicas import Logicas
from models.Expresion.Primitivo import Primitivo
from models.Expresion.Id import Id
from models.Expresion.If_Ternario import If_ternario
from models.Expresion.BrazoTer import BrazoTer
from models.Expresion.MatchTer import MatchTer
from models.Expresion.As import As
from models.Expresion.Nativas.Abs import Abs
from models.Expresion.Nativas.Sqrt import Sqrt
from models.Expresion.Nativas.ToStringOwned import ToStringOwned
from models.Expresion.Nativas.Clone import Clone
from models.Expresion.Nothing import Nothing
#Instrucciones
from models.Instruction.Println import Println
from models.Instruction.Declaracion import Declaracion
from models.Instruction.Asignacion import Asignacion
from models.Instruction.If import If
from models.Instruction.Brazo import Brazo
from models.Instruction.Match import Match
from models.Instruction.Loop import Loop
from models.Instruction.Return import Return
from models.Instruction.Break import Break
from models.Instruction.Continue import Continue
from models.Instruction.While import While
from models.Instruction.Funcion import Funcion
from models.Instruction.Call import Call
from models.Instruction.ForIn import ForIn
from models.Expresion.Rango import Rango
from models.Expresion.CharArray import CharArray
#structs
from models.Instruction.Struct.SaveStruct import SaveStruct
from models.Expresion.Struct.ExpStruct import ExpStruct
from models.Instruction.Struct.DecStruct import DecStruct
from models.Expresion.Struct.DecStructExp import DecStructExp
from models.Expresion.Struct.AccesStruct import AccesStruct
from models.Instruction.Struct.Modi_Var_Struct import ModiVarStruct
#Modulos
from models.Instruction.Modulo.SaveModulo import SaveModulo
from models.Expresion.Modulo.AccesModulo import AccesModulo
    #vectores
from models.Expresion.Vector.vecI import vecI
from models.Expresion.Vector.AccesVec import AccesVec
from models.Instruction.Vector.Push import Push
from models.Instruction.Vector.Insert import Insert
from models.Expresion.Vector.Remove import Remove
from models.Expresion.Vector.Contains import Contains
from models.Expresion.Vector.Len import Len
from models.Expresion.Vector.Capacity import Capacity
from models.Instruction.Vector.DecVector import DecVector
    #arreglos
from models.Instruction.Arreglo.DecArreglo import DecArreglo
from models.Expresion.Arreglo.Arreglo import Arreglo
from models.Expresion.Arreglo.DimensionalArreglo import DimensionalArreglo
#ayudas
from models.TablaSymbols.Tipos import Tipos


tokens = lexer.tokens

# EXPRESION : term MAS term
#            | term MENOS term
#            | term
# term : factor


# precedencia

precedence = (

    ('left', 'or'),
    ('left', 'and'),
    ('left','igualigual','diferente','menor','menorigual','mayor','mayorigual'),
    ('left', 'menos', 'mas'),
    ('left', 'multi', 'div','mod'),
    ('right', 'not'),
    ('right', 'UNARIO'),
)


def p_inicio(p):
    """
    INICIO : INSTRUCCIONES_RUST
    """
    p[0] = Ast(p[1])
def p_rust_inst_lista(p):
    """INSTRUCCIONES_RUST : INSTRUCCIONES_RUST INST_RUST"""
    p[1].append(p[2])
    p[0] = p[1]

def p_rust_inst_instruccion(p):
    """INSTRUCCIONES_RUST : INST_RUST"""
    p[0] = [p[1]]
def p_rust_inst(p):
    """INST_RUST : MODULO
                 | FUNCION
                 | STRUCT"""
    p[0]=p[1]

def p_instrucciones_lista(p):
    """
    INSTRUCCIONES : INSTRUCCIONES INSTRUCCION
    """
    p[1].append(p[2])
    p[0] = p[1]
    
def p_instrucciones_instruccion(p):
    """
    INSTRUCCIONES : INSTRUCCION
    """
    p[0] = [p[1]]

def p_instruccion(p):
    """
    INSTRUCCION : PRINT puntoycoma
        | DECLARACION puntoycoma
        | ASIGNACION puntoycoma
        | IF
        | MATCH
        | CONTINUE puntoycoma
        | RETURN puntoycoma
        | BREAK puntoycoma
        | WHILE
        | EXPRESION
        | CALL puntoycoma
        | FUNCION
        | DECVECTOR puntoycoma
        | PUSH puntoycoma
        | INSERT puntoycoma
        | DECARREGLO puntoycoma
        | FORIN
        | STRUCT
        | DECSTRUCT puntoycoma
        | MOD_VAR_STRUCT puntoycoma
        | REMOVE puntoycoma
        | MODULO
        | ACCESO_MOD puntoycoma
    """
    #Anotaciones:
        #LOOP ES TANTO INSTRUCCION COMO EXPRESION, TIENE GETVALOR,GETTIPO Y EJECUTAR ESTE SE ENCUENTRA DECLARADO EN EXPRESION
        #La mayoria de expresiones tienen un ejecutar que no hace nada, es por si realiza una expresion afuera de cualquier estructura
            #en rust es permitido
    p[0] = p[1]

def p_expresion_aritmeticas(p):
    """
    EXPRESION : EXPRESION mas EXPRESION 
            |   EXPRESION menos EXPRESION
            |   EXPRESION div EXPRESION
            |   EXPRESION multi EXPRESION
            |   EXPRESION mod EXPRESION  
            |   i64 dospuntos dospuntos pow para EXPRESION coma EXPRESION parc
            |   f64 dospuntos dospuntos powf para EXPRESION coma EXPRESION parc
    """
    # p contiene los elementos de la gramatica
    #
    # EXPRESION : term MAS term
    #   p[0]     : p[1] p[2] p[3]
    #
    if p[2] != ':':
        p[0] = Aritmeticas(exp1=p[1], operador=p[2], exp2=p[3], expU=False, linea=p.lineno(1), columna=0)
    else:
        p[0] = Aritmeticas(exp1=p[6], operador=p[4], exp2=p[8], expU=False, linea=p.lineno(1), columna=0)

def p_factor_unario(p):
    """
    EXPRESION : menos EXPRESION %prec UNARIO
    """
    p[0] = Aritmeticas(exp1=p[2], operador=p[1], exp2=None, expU=True, linea=p.lineno(1), columna=0)

def p_expresion_relacionales(p):
    """
    EXPRESION :  EXPRESION mayor EXPRESION
            |   EXPRESION menor EXPRESION
            |   EXPRESION mayorigual EXPRESION
            |   EXPRESION menorigual EXPRESION
            |   EXPRESION igualigual EXPRESION
            |   EXPRESION diferente EXPRESION
    """
    p[0]= Relacionales(exp1=p[1], operador=p[2], exp2=p[3], linea=p.lineno(1), columna=0)

def p_expresion_logicas(p):
    """
    EXPRESION :  EXPRESION and EXPRESION
            |   EXPRESION or EXPRESION
    """
    p[0] = Logicas(exp1=p[1], operador=p[2], exp2=p[3],expU=False, linea=p.lineno(1), columna=0)
def p_expresion_logicas_not(p):
    """
    EXPRESION :  not EXPRESION
    """
    p[0] = Logicas(exp1=p[2], operador=p[1], exp2=None, expU=True, linea=p.lineno(1), columna=0)

def p_EXPRESION_par(p):
    """
    EXPRESION : para EXPRESION parc
    """
    p[0] = p[2]
#PRODUCCION PARA EXPRESIONES DE UN SOLO ELEMENTO=====================================================================================0
def p_exp_one_element(p):
    """
    EXPRESION : TIPODATO
        | ID
        | IF_TER
        | MATCH_TER
        | LOOP
        | CAST_AS
        | ABS
        | CLONE
        | SQRT
        | TO_STRING_OWNED
        | CALL
        | REMOVE
        | CONTAINS
        | LEN
        | CAPACITY
        | ACCESVEC
        | ACCESO_STRUCT
        | ACCESO_MOD
    """
    p[0]=p[1]
#CONJEXP=====================================================================================0
def p_cexp_list(p):
    """CONJEXP : CONJEXP coma ELCONJ"""
    p[1].append(p[3])
    p[0]=p[1]
def p_cexp(p):
    """CONJEXP : ELCONJ"""
    p[0] = [p[1]]
def p_element_cexp(p):
    """ELCONJ : ampersand ELCONJ"""
    p[0]=p[2]
def p_elementcexp(p):
    """ELCONJ : EXPRESION
            | VECI
            | ARREGLO
            | ampersand mut EXPRESION"""
    if p[1]!="&":
        p[0] = p[1]
    else:
        p[3].paso_parametro = True
        p[0]=p[3]
#tipo de dato=====================================================================================0
def p_tipo_dato(p):
    """
    TIPODATO : entero
        | decimal
        | cadena
        | true
        | false
    """
    p[0] = Primitivo(p[1], p.lineno(1), 0)
#dato tipo id
def p_id(p):
    """
    ID : id
    """  
    p[0] = Id(p[1],p.lineno(1), 0)

def p_char(p):
    """
    TIPODATO : caracter
    """
    p[0] = Primitivo(p[1], p.lineno(1), 0,"char")
#tipo de variable=====================================================================================0
def p_tipo_var(p):
    """
    TIPOVAR : i64
        | f64
        | bool
        | string
        | char
        | str
        | usize
    """
    p[0] = p[1]
#If ternario=====================================================================================0
def p_if_ternario(p):
    """
    IF_TER : if  EXPRESION  llavea INSTRUCCIONES EXPRESION llavec
        | if  EXPRESION  llavea EXPRESION llavec
    """
    if len(p)==7:
        p[0] = If_ternario(exp=p[2],bloque1=p[4],exp1b=p[5],bloque2=[],exp2b=None,line=p.lineno(1), column=0)
    else:
        p[0] = If_ternario(exp=p[2], bloque1=[], exp1b=p[4], bloque2=[], exp2b=None, line=p.lineno(1), column=0)
def p_if_else_ternario(p):
    """
    IF_TER : if  EXPRESION  llavea INSTRUCCIONES EXPRESION llavec else llavea INSTRUCCIONES EXPRESION llavec
           | if  EXPRESION  llavea  EXPRESION llavec else llavea EXPRESION llavec
    """
    if len(p)==12:
        p[0] = If_ternario(exp=p[2], bloque1=p[4],exp1b=p[5], bloque2=p[9],exp2b=p[10], line=p.lineno(1), column=0)
    else:
        p[0] = If_ternario(exp=p[2], bloque1=[], exp1b=p[4], bloque2=[], exp2b=p[8], line=p.lineno(1), column=0)
def p_if_else_ternario_2(p):
    """
    IF_TER : if  EXPRESION  llavea  EXPRESION llavec else llavea INSTRUCCIONES EXPRESION llavec
           | if  EXPRESION  llavea  INSTRUCCIONES EXPRESION llavec else llavea EXPRESION llavec
    """
    if p[5]=="}":
        p[0] = If_ternario(exp=p[2], bloque1=[],exp1b=p[4], bloque2=p[8],exp2b=p[9], line=p.lineno(1), column=0)
    else:
        p[0] = If_ternario(exp=p[2], bloque1=p[4], exp1b=p[5], bloque2=[], exp2b=p[9], line=p.lineno(1), column=0)
def p_if_else_if_ternario(p):
    """
    IF_TER : if EXPRESION  llavea INSTRUCCIONES EXPRESION llavec else IF_TER
        | if EXPRESION  llavea EXPRESION llavec else IF_TER
    """
    if len(p)==9:
        p[0] = If_ternario(exp=p[2], bloque1=p[4],exp1b=p[5], bloque2=[], exp2b=p[8],line=p.lineno(1), column=0)
    else:
        p[0] = If_ternario(exp=p[2], bloque1=[], exp1b=p[4], bloque2=[], exp2b=p[7], line=p.lineno(1), column=0)
#Match ternario=====================================================================================
def p_matchTer(p):
    """
    MATCH_TER : match EXPRESION llavea BRAZOS_TER guionbajo igual mayor EXPRESION coma llavec
        |  match EXPRESION llavea guionbajo igual mayor EXPRESION coma llavec
    """
    if p[4]!="_":
        p[0] = MatchTer(exp=p[2],brazos=p[4],default=p[8], line=p.lineno(1), column=0)
    else:
        p[0] = MatchTer(exp=p[2],brazos=[], default=p[7], line=p.lineno(1), column=0)
def p_brazosTer_list(p):
    """
    BRAZOS_TER : BRAZOS_TER BRAZO_TER
        | BRAZO_TER
    """
    if len(p)==3:
        p[1].append(p[2])
        p[0] = p[1]
    elif len(p)==2:
        p[0] = [p[1]]

def p_brazoTer(p):
    """
    BRAZO_TER : CONJEXPM igual mayor EXPRESION coma
    """
    p[0] = BrazoTer(cExp=p[1], bloque=p[4], line=p.lineno(1), column=0)
#AS=====================================================================================
def p_as(p):
    """CAST_AS : EXPRESION as TIPOVAR"""
    p[0]=As(exp=p[1],tipocast=p[3],line=p.lineno(1), column=0)
#ABS=====================================================================================
def p_abs(p):
    """ABS : EXPRESION punto abs para parc"""
    p[0]=Abs(exp=p[1], line=p.lineno(1), column=0)
def p_abs_id(p):
    """ABS : id punto abs para parc"""
    exp = Id(p[1], p.lineno(1), 0)
    p[0] = Abs(exp=exp, line=p.lineno(1), column=0)
#CLONE=====================================================================================
def p_clone(p):
    """CLONE : EXPRESION punto clone para parc"""
    p[0]=Clone(exp=p[1], line=p.lineno(1), column=0)
def p_clone_id(p):
    """CLONE : id punto clone para parc"""
    exp = Id(p[1], p.lineno(1), 0)
    p[0] = Clone(exp=exp, line=p.lineno(1), column=0)
def p_clone_vec(p):
    """CLONE : id INDEXS punto clone para parc"""
    exp = AccesVec(id=p[1], cIndex=p[2], cIds=[], line=p.lineno(1), column=0)
    p[0] = Clone(exp=exp, line=p.lineno(1), column=0)
#Sqrt=====================================================================================
def p_sqrt(p):
    """SQRT : EXPRESION punto sqrt para parc"""
    p[0] = Sqrt(exp=p[1], line=p.lineno(1), column=0)
def p_sqrt_id(p):
    """SQRT : id punto sqrt para parc"""
    exp = Id(p[1], p.lineno(1), 0)
    p[0] = Sqrt(exp=exp, line=p.lineno(1), column=0)
#Sqrt=====================================================================================
def p_tostrig_owned_id(p):
    """TO_STRING_OWNED : EXPRESION punto toString para parc
        | EXPRESION punto toOwned para parc
    """
    p[0] = ToStringOwned(exp=p[1], line=p.lineno(1), column=0)
def p_tostring_owned2(p):
    """TO_STRING_OWNED : id punto toString para parc
        | id punto toOwned para parc"""
    exp = Id(p[1], p.lineno(1), 0)
    p[0] = ToStringOwned(exp=exp, line=p.lineno(1), column=0)


#Instrucciones------------------------------------------------------------------------------------
def p_println(p):
    """
    PRINT : println para EXPRESION parc
        | println para EXPRESION coma CONJEXP parc
    """
    if(p[4]==")"):
        p[0] = Println(exp=p[3],cExp=[], linea=p.lineno(1), columna=0)
    else:
        p[0] = Println(exp=p[3],cExp=p[5],linea= p.lineno(1), columna= 0)

#Declaraciones=====================================================================================
def p_declaracion_t1(p):
    """
    DECLARACION : let mut id dospuntos TIPOVAR igual EXPRESION
                | let mut id igual EXPRESION
    """
    if(p[4]==":"):
        p[0]=Declaracion(mut=True,id=p[3],tipo=p[5],exp=p[7],linea=p.lineno(1), columna=0)
    else:
        p[0]=Declaracion(mut=True,id=p[3],tipo="",exp=p[5],linea=p.lineno(1), columna=0)

def p_declaracion_t2(p):
    """
    DECLARACION : let id dospuntos TIPOVAR igual EXPRESION
                | let id igual EXPRESION
    """
    if (p[3] == ":"):
        p[0] = Declaracion(mut=False, id=p[2], tipo=p[4], exp=p[6], linea=p.lineno(1), columna=0)
    else:
        p[0] = Declaracion(mut=False, id=p[2], tipo="", exp=p[4], linea=p.lineno(1), columna=0)

def p_declaracion_t3(p):
    """
    DECLARACION : let mut id dospuntos TIPOVAR
    """
    if (p[2] == "mut"):
        p[0] = Declaracion(mut=True, id=p[2], tipo=[4], exp=None, linea=p.lineno(1), columna=0)
    else:
        p[0] = Declaracion(mut=False, id=p[2], tipo=[4], exp=None, linea=p.lineno(1), columna=0)
#Asignaciones=====================================================================================
def p_asignaciones(p):
    """
    ASIGNACION : id igual EXPRESION
        | id INDEXS igual EXPRESION 
        | id INDEXS punto CONJ_ACCES igual EXPRESION  
    """  #el segundo es para los vectores  vector1[1][3]="hola";   #*******************************************************
    if p[2]=="=":
        p[0] = Asignacion(id=p[1],cIndex=[],cIds=[],exp=p[3],linea=p.lineno(1), columna=0)
    elif p[3]!=".":
        p[0] = Asignacion(id=p[1], cIndex=p[2],cIds=[], exp=p[4], linea=p.lineno(1), columna=0)
    else:
        p[0] = Asignacion(id=p[1], cIndex=p[2],cIds=p[4],exp=p[6], linea=p.lineno(1), columna=0)

def p_asignaciones_vec(p):
    """ASIGNACION : id igual  Vec dospuntos dospuntos new para parc
            | id igual Vec dospuntos dospuntos withcapacity para EXPRESION parc"""
    if len(p)==9:
        p[0] = Asignacion(id=p[1], cIndex=[], cIds=[], exp=[], linea=p.lineno(1), columna=0)
    else:
        p[0] = Asignacion(id=p[1], cIndex=[], cIds=[], exp=[p[8]], linea=p.lineno(1), columna=0)
#If=====================================================================================
def p_if(p):
    """
    IF : if  EXPRESION  BLOQUE_INST
    """
    p[0] = If(exp=p[2],bloque1=p[3],bloque2=[],line=p.lineno(1), column=0)
def p_if_else(p):
    """
    IF : if  EXPRESION  BLOQUE_INST else BLOQUE_INST
    """
    p[0] = If(exp=p[2], bloque1=p[3], bloque2=p[5], line=p.lineno(1), column=0)
def p_if_else_if(p):
    """
    IF : if EXPRESION  BLOQUE_INST else IF
    """
    p[0] = If(exp=p[2], bloque1=p[3], bloque2=[p[5]], line=p.lineno(1), column=0)

#match=====================================================================================
def p_match_1(p):
    """
    MATCH : match EXPRESION llavea BRAZOS guionbajo igual mayor BLOQUE_INST llavec
        | match EXPRESION llavea guionbajo igual mayor BLOQUE_INST llavec
    """
    if p[4]!="_":
        p[0] = Match(exp=p[2],lbrazos=p[4],default=p[8], line=p.lineno(1), column=0)
    else:
        p[0] = Match(exp=p[2], lbrazos=[], default=p[8], line=p.lineno(1), column=0)
def p_match_2(p):
    """
    MATCH : match EXPRESION llavea BRAZOS guionbajo igual mayor INSTRUCCION_1LINE coma llavec
        |  match EXPRESION llavea guionbajo igual mayor INSTRUCCION_1LINE coma llavec
    """
    if p[4]!="_":
        p[0] = Match(exp=p[2],lbrazos=p[4],default=[p[8]], line=p.lineno(1), column=0)
    else:
        p[0] = Match(exp=p[2], lbrazos=[], default=[p[8]], line=p.lineno(1), column=0)
def p_instruction_1oneline(p):
    """INSTRUCCION_1LINE : PRINT
                    | DECLARACION
                    | ASIGNACION
                    | PUSH
                    | INSERT
                    | DECARREGLO
                    | DECVECTOR
                    | DECSTRUCT
                    | MOD_VAR_STRUCT"""
    p[0]=p[1]
def p_brazos_list(p):
    """
    BRAZOS : BRAZOS BRAZO
    """
    p[1].append(p[2])
    p[0] = p[1]
def p_brazos_brazo(p):
    """
    BRAZOS : BRAZO
    """
    p[0]=[p[1]]
def p_brazo(p):
    """
    BRAZO : CONJEXPM igual mayor BLOQUE_INST
        | CONJEXPM igual mayor INSTRUCCION_1LINE coma
    """
    if type(p[4]) in (tuple,list):
        p[0] = Brazo(cExp=p[1],bloque=p[4], line=p.lineno(1), column=0)
    else:
        p[0] = Brazo(cExp=p[1], bloque=[p[4]], line=p.lineno(1), column=0)
def p_conj_exp_match_list(p):
    """CONJEXPM : CONJEXPM bvertical EXPRESION"""
    p[1].append(p[3])
    p[0]=p[1]
def p_conj_exp_match_exp(p):
#bloque instrucciones=====================================================================================
    """CONJEXPM : EXPRESION"""
    p[0]=[p[1]]
#Loop=====================================================================================
def p_loop(p):
    """LOOP : loop BLOQUE_INST"""
    p[0] = Loop(bloque=p[2],line=p.lineno(1),column=0)
#break=====================================================================================
def p_break(p):
    """BREAK : break"""
    p[0] = Break(exp=None,line=p.lineno(1),column=0)
def p_break2(p):
    """BREAK : break EXPRESION"""
    p[0] = Break(exp=p[2],line=p.lineno(1),column=0)
#Continue =====================================================================================
def p_continue(p):
    """CONTINUE : continue"""
    p[0] = Continue(line=p.lineno(1),column=0)
#return =====================================================================================
def p_return(p):
    """RETURN : return EXPRESION"""
    p[0] = Return(exp=p[2],line=p.lineno(1),column=0)
def p_return_2(p):
    """RETURN : return"""
    p[0] = Return(exp=None,line=p.lineno(1),column=0)
#while =====================================================================================
def p_while(p):
    """WHILE : while EXPRESION BLOQUE_INST"""
    p[0]= While(exp=p[2],bloque=p[3],line=p.lineno(1),column=0)
def p_bloque_instrucciones(p):
    """
    BLOQUE_INST : llavea  INSTRUCCIONES llavec
    """
    p[0]=p[2]
#Funcion=====================================================================================
def p_funcion(p):
    """
    FUNCION : fn id para LISTAPARAMETROS parc menos mayor TIPOVAR BLOQUE_INST
        | fn id para LISTAPARAMETROS parc BLOQUE_INST
    """
    if p[6]=="-":
        p[0]=Funcion(id=p[2],lparametros=p[4],tipo=p[8],bloque=p[9],line=p.lineno(1),column=0)
    else:
        p[0]=Funcion(id=p[2],lparametros=p[4],tipo="",bloque=p[6],line=p.lineno(1),column=0)
def p_funcion2(p):
    """
    FUNCION : fn id para  parc menos mayor TIPOVAR BLOQUE_INST
        | fn id para  parc BLOQUE_INST
    """
    if p[5]=="-":
        p[0]=Funcion(id=p[2],lparametros=[],tipo=p[7],bloque=p[8],line=p.lineno(1),column=0)
    else:
        p[0]=Funcion(id=p[2],lparametros=[],tipo="",bloque=p[5],line=p.lineno(1),column=0)
def p_funcion3(p):
    #    ->  NameStruct {}     |    -> Vec < ID >
    """
    FUNCION : fn id para LISTAPARAMETROS parc menos mayor id BLOQUE_INST
    """
    p[0]=Funcion(id=p[2],lparametros=p[4],tipo=p[8],bloque=p[9],line=p.lineno(1),column=0)
def p_fucion_rvec(p):
    """
        FUNCION : fn id para LISTAPARAMETROS parc menos mayor VEC BLOQUE_INST
    """
    tipo = p[8]["tipo"]
    p[0] = Funcion(id=p[2], lparametros=p[4], tipo=tipo, bloque=p[9], line=p.lineno(1), column=0)
    p[0].tipo_return = Tipos.VECTOR


def p_lista_parametros(p):
    """LISTAPARAMETROS : LISTAPARAMETROS coma PARAMETRO"""
    p[1].append(p[3])
    p[0]=p[1]
def p_lista_parametros_parametro(p):
    """LISTAPARAMETROS : PARAMETRO"""
    p[0]=[p[1]]
def p_parametro(p):
    """PARAMETRO : id dospuntos TIPOVAR
                | mut id dospuntos TIPOVAR
    """
    if p[1]!="mut":
        p[0] = Declaracion(mut=False, id=p[1], tipo=p[3], exp=None, linea=p.lineno(1), columna=0)
    else:
        p[0]=Declaracion(mut=True,id=p[2],tipo=p[4],exp=None,linea=p.lineno(1),columna=0)
def p_parametro2(p):
    """PARAMETRO :    id dospuntos ampersand mut cora TIPOVAR corc
                    | id dospuntos ampersand mut DIMENSION_ARR
        """
    if len(p)==8:
        p[0]=DecArreglo(mut=True,id=p[1],arrDimensional=None,array=None,line=p.lineno(1),column=0)
    elif len(p)==6:
        p[0] = DecArreglo(mut=True, id=p[1], arrDimensional=p[5], array=None, line=p.lineno(1), column=0)
    p[0].dec_paso_parametro=True
def p_parametro3(p):
    """PARAMETRO : id dospuntos ampersand mut VEC
                | mut id dospuntos ampersand VEC"""
    if p[4]=="mut":
        profundidad = p[5]["profundidad"]
        tipo = p[5]["tipo"]
        p[0]=DecVector(mut=True,id=p[1],tipo=tipo,vecI=None,capacity=None,line=p.lineno(1),column=0)
        p[0].profundidad=profundidad
    else:
        profundidad = p[5]["profundidad"]
        tipo = p[5]["tipo"]
        p[0] = DecVector(mut=False, id=p[2], tipo=tipo, vecI=None, capacity=None, line=p.lineno(1), column=0)
        p[0].profundidad = profundidad
    p[0].dec_paso_parametro = True


def p_parametro4(p):
    """PARAMETRO : id dospuntos VEC
            | mut id dospuntos VEC
    """
    if p[1]!="mut":
        profundidad = p[3]["profundidad"]
        tipo = p[3]["tipo"]
        p[0] = DecVector(mut=False, id=p[1], tipo=tipo, vecI=None, capacity=None, line=p.lineno(1), column=0)
        p[0].profundidad = profundidad
    else:
        profundidad = p[4]["profundidad"]
        tipo = p[4]["tipo"]
        p[0] = DecVector(mut=True, id=p[2], tipo=tipo, vecI=None, capacity=None, line=p.lineno(1), column=0)
        p[0].profundidad = profundidad

def p_parametro5(p):
    """PARAMETRO : id dospuntos ampersand mut id"""
    p[0]=DecStruct(mut=True,id=p[1],exp=None, line=p.lineno(1), column=0)
#Call
def p_call(p):
    """CALL : id para CONJEXP parc
        | id para parc
    """
    if p[3]!=")":
        p[0]=Call(id=p[1],cExp=p[3], line=p.lineno(1), column=0)
    else:
        p[0]=Call(id=p[1],cExp=[], line=p.lineno(1), column=0)

#DECLARACION DE VECTOR
def p_defvector_1(p):
    """
    DECVECTOR : let id igual VECI
        | let mut id igual VECI
    """
    if p[2] != "mut":
        p[0]=DecVector(mut=False,id=p[2],tipo=None,vecI=p[4],capacity=None,line=p.lineno(1), column=0)
    else:
        p[0]=DecVector(mut=True,id=p[3],tipo=None,vecI=p[5],capacity=None,line=p.lineno(1), column=0)
def p_defvector_2(p):
    """
    DECVECTOR : let id dospuntos VEC igual VECI
        | let mut id dospuntos VEC igual VECI
    """
    if p[2] != "mut":
        profundidad = p[4]["profundidad"]
        tipo = p[4]["tipo"]
        p[0]=DecVector(mut=False,id=p[2],tipo=tipo,vecI=p[6],capacity=None,line=p.lineno(1), column=0)
    else:
        profundidad = p[5]["profundidad"]
        tipo = p[5]["tipo"]
        p[0]=DecVector(mut=True,id=p[3],tipo=tipo,vecI=p[7],capacity=None,line=p.lineno(1), column=0)

def p_devector_3(p):
    """DECVECTOR : let id dospuntos VEC igual Vec dospuntos dospuntos FUNCVEC
                | let mut id dospuntos VEC igual Vec dospuntos dospuntos FUNCVEC
                | let id igual Vec dospuntos dospuntos FUNCVEC
                | let mut id igual Vec dospuntos dospuntos FUNCVEC"""
    if p[2]!="mut":
        if len(p)==10:  #con vec < tipovar >
            profundidad= p[4]["profundidad"]
            tipo = p[4]["tipo"]

            p[0] = DecVector(mut=False,id=p[2],tipo=tipo, vecI=None, capacity=p[9], line=p.lineno(1), column=0)
            p[0].profundidad = profundidad
        else:
            p[0] = DecVector(mut=False, id=p[2], tipo=None, vecI=None, capacity=p[7], line=p.lineno(1), column=0)
    else:
        if len(p)==11:  #con vec < tipovar >
            profundidad = p[5]["profundidad"]
            tipo = p[5]["tipo"]

            p[0] = DecVector(mut=True,id=p[3],tipo=tipo,  vecI=None, capacity=p[10], line=p.lineno(1), column=0)
            p[0].profundidad = profundidad
        else:
            p[0] = DecVector(mut=True, id=p[3], tipo=None, vecI=None, capacity=p[8], line=p.lineno(1), column=0)

def p_dimensional_vector_recur(p):
    """VEC : Vec menor VEC mayor"""
    p[0]=p[3]
    p[0] = {"profundidad": (1+p[0]["profundidad"]), "tipo": p[0]["tipo"]}
    print(p[0])
def p_dimensional_vector(p):
    """VEC : Vec menor TIPOVAR mayor"""
    p[0]=p[3]
    p[0] = {"profundidad": 1, "tipo": p[0]}
    print(p[0])
def p_dimensional_vetor2(p):
    """VEC : Vec menor CONJ_ACCES_MOD mayor """  #Aqui va tanto los vectores tipo id (que almacenan structs) y los id::id:id que almacenan structs de modulos
    p[0]=p[3][len(p[3])-1]

    p[0]={"profundidad":1,"tipo":p[0]}
    print(p[0])


def p_vectori(p):
    #veci  =   vec!
    """VECI : vecI cora CONJVECI  corc
            | vecI cora EXPRESION puntoycoma EXPRESION corc"""
    if p[4]!=";":
        p[0]=vecI(cExp=p[3],exp=None,multiplicador=None,line=p.lineno(1), column=0)
        if isinstance(p[3][0],vecI):
            p[0].profundidad=p[3][0].profundidad+1
    else:
        p[0]=vecI(cExp=None,exp=p[3],multiplicador=p[5],line=p.lineno(1), column=0)

def p_conjveci_lista(p):
    #conjunto de expresiones cojveci =   conjutno de expresiones conjveci coma elemento vec
    """ CONJVECI : CONJVECI  coma ELVEC"""
    p[1].append(p[3])
    p[0]=p[1]
def p_conjvei_element(p):
    """CONJVECI : ELVEC"""
    p[0]=[p[1]]
def p_elemento_vec(p):
    """ELVEC : EXPRESION
            | VECI"""
    p[0]=p[1]
def p_func_vec(p):
    """FUNCVEC : new para parc
            | withcapacity para EXPRESION parc """
    if p[1]=="new":
        p[0]=None
    else:
        p[0]=p[3]
def p_instv_push(p):
    """PUSH : id punto push para EXPRESION parc
            |  id punto push para VECI parc
            | id punto push para STRUCT_EXP parc"""
    p[0] = Push(id=p[1],exp=p[5],line=p.lineno(1), column=0)
def p_instv_insert(p):
    """INSERT : id punto insert para EXPRESION coma EXPRESION parc """
    p[0]=Insert(id=p[1],index=p[5],exp=p[7],line=p.lineno(1), column=0)
def p_instv_remove(p): #esta va en expresiones
    """REMOVE : id punto remove para EXPRESION parc"""
    p[0]= Remove(id=p[1],index=p[5],line=p.lineno(1), column=0)
def p_instv_contains(p):
    """CONTAINS : id punto contains para ampersand EXPRESION parc
                | id punto contains para EXPRESION parc"""
    if len(p)==8:
        p[0]=Contains(id=p[1],exp=p[6],line=p.lineno(1), column=0)
    else:
        p[0] = Contains(id=p[1], exp=p[5], line=p.lineno(1), column=0)
def p_instv_len(p):
    """LEN : EXPRESION punto len para parc"""
    p[0] = Len(id="",exp=p[1],line=p.lineno(1), column=0)
def p_instv_len2(p):
    """LEN : id INDEXS punto len para parc"""
    exp = AccesVec(id=p[1], cIndex=p[2], cIds=[], line=p.lineno(1), column=0)
    p[0] = Len(id=p[1],exp=exp, line=p.lineno(1), column=0, cIndex=p[2])
def p_instv_len3(p):
    """LEN : id punto len para parc """
    exp=Id(p[1],linea=p.lineno(1),columna=0)
    p[0]=Len(id=p[1],exp=exp,line=p.lineno(1), column=0)


def p_instv_capacity(p):
    """CAPACITY : id punto capacity para parc"""
    p[0]=Capacity(id=p[1],line=p.lineno(1), column=0)
def p_instv_acces(p):   #*******************************************************************************
    """ACCESVEC : id INDEXS
                | id INDEXS punto CONJ_ACCES"""
    if len(p)==3:
        p[0]=AccesVec(id=p[1],cIndex=p[2],cIds=[],line=p.lineno(1), column=0)
    else:
        p[0]=AccesVec(id=p[1],cIndex=p[2],cIds=p[4],line=p.lineno(1), column=0)
def p_index_acces_list(p):
    """INDEXS : INDEXS cora EXPRESION corc"""
    p[1].append(p[3])
    p[0]=p[1]
def p_index_acces(p):
    """INDEXS : cora EXPRESION corc"""
    p[0]=[p[2]]

#ARREGLOS
def p_dec_arreglo1(p):
    """DECARREGLO : let id dospuntos DIMENSION_ARR igual ARREGLO
                | let mut id dospuntos DIMENSION_ARR igual ARREGLO """
    if p[3]==":":
        p[0]=DecArreglo(mut=False,id=p[2],arrDimensional=p[4],array=p[6],line=p.lineno(1), column=0)
    else:
        p[0]=DecArreglo(mut=True,id=p[3],arrDimensional=p[5],array=p[7],line=p.lineno(1), column=0)
def p_dec_arreglo2(p):
    """DECARREGLO : let id igual ARREGLO
                | let mut id igual ARREGLO"""
    if p[3]=="=":
        p[0] = DecArreglo(mut=False, id=p[2], arrDimensional=None, array=p[4], line=p.lineno(1), column=0)
    else:
        p[0] = DecArreglo(mut=True, id=p[3], arrDimensional=None, array=p[5], line=p.lineno(1), column=0)
def p_dimension_arreglo_multidimensional(p):
    """DIMENSION_ARR : cora DIMENSION_ARR puntoycoma EXPRESION corc """
    p[0] = DimensionalArreglo(tipo="",dimArr=p[2], Dimensional=p[4], line=p.lineno(1), column=0)
def p_dimension_arreglo_unidimensional(p):
    """DIMENSION_ARR : cora TIPOVAR puntoycoma EXPRESION corc
                    | cora id puntoycoma EXPRESION corc"""  #para los structs [ PersonajeStruct ; 3]
    p[0]=DimensionalArreglo(tipo=p[2],dimArr=None,Dimensional=p[4],line=p.lineno(1), column=0)
def p_arreglo_conj(p):
    """ARREGLO : cora CONT_ARR corc"""
    p[0]=Arreglo(cExp=p[2],exp=None,multi=None,line=p.lineno(1), column=0)
    if isinstance(p[2][0],Arreglo):
        p[0].profundidad=p[2][0].profundidad+1
def p_arreglo_multi(p):
    """ARREGLO : cora EXPRESION puntoycoma EXPRESION corc"""
    p[0]=Arreglo(cExp=None,exp=p[2],multi=p[4],line=p.lineno(1), column=0)
def p_cont_arreglo(p):
    """CONT_ARR : CONT_ARR coma ELARR"""
    p[1].append(p[3])
    p[0]=p[1]
def p_cont_arreglo_u(p):
    """CONT_ARR : ELARR"""
    p[0]=[p[1]]

def p_elemento_arreglo(p):
    """ELARR : ARREGLO
            | EXPRESION
            | STRUCT_EXP"""
    p[0]=p[1]


# Forin
def p_forin(p):
    """FORIN : for id in ARRFOR BLOQUE_INST"""
    p[0]=ForIn(id=p[2],arreglo=p[4],cInst=p[5],line=p.lineno(1), column=0)

def p_arrfor(p):
    """ARRFOR : CHARS
            | ARREGLO
            | VECI  
            | RANGO
            | ID"""   #-----------------------------CAMBIAR ------------ ARREGLO POR EXP
    p[0]=p[1]
def p_charArr(p):
    """CHARS : EXPRESION punto chars para parc"""
    p[0]=CharArray(exp=p[1], line=p.lineno(1), column=0)
def p_charArr_id(p):
    """CHARS : id punto chars para parc"""
    exp = Id(p[1], p.lineno(1), 0)
    p[0] = CharArray(exp=exp, line=p.lineno(1), column=0)
def p_rangoArr(p):
    """RANGO : EXPRESION punto punto EXPRESION"""
    p[0]=Rango(exp1=p[1],exp2=p[4], line=p.lineno(1), column=0)

#STRUCTS  reconocimiento
def p_struct(p):
    """STRUCT : struct id llavea CONTENT_STRUCT llavec"""
    p[0]=SaveStruct(id=p[2],cInst=p[4], line=p.lineno(1), column=0)
def p_struct_content(p):
    """CONTENT_STRUCT : CONTENT_STRUCT coma ELSTRUCT"""
    p[1].append(p[3])
    p[0]=p[1]
def p_struc_content_u(p):
    """CONTENT_STRUCT : ELSTRUCT"""
    p[0] = [p[1]]
def p_element_pub_struc(p):
    """ELSTRUCT : pub ELSTRUCT"""
    p[2].changeAcces(1)
    p[0]=p[2]
def p_elemento_struct(p):
    """ELSTRUCT : id dospuntos TIPOVAR
                | id dospuntos id"""
                #el ultimo es para los elementos de tipo struct
    p[0]=Declaracion(mut=True,id=p[1],tipo=p[3],exp=None,linea=p.lineno(1), columna=0)
#declaracion de variables structs
def p_dec_var_struct(p):
    """DECSTRUCT : let id igual STRUCT_EXP
                    | let mut id igual STRUCT_EXP"""
    if p[2]!="mut":
        p[0]=DecStruct(mut=False,id=p[2],exp=p[4],line=p.lineno(1), column=0)
    else:
        p[0] = DecStruct(mut=True, id=p[3],exp=p[5], line=p.lineno(1), column=0)
def p_dec_var_struct2(p):
    """DECSTRUCT : let id dospuntos id igual STRUCT_EXP
                    | let mut id dospuntos id igual STRUCT_EXP"""
    if p[2]!="mut":
        p[0]=DecStruct(mut=False,id=p[2],exp=p[6],line=p.lineno(1), column=0)
    else:
        p[0] = DecStruct(mut=True, id=p[3],exp=p[7], line=p.lineno(1), column=0)
def p_dec_var_struct_exp(p):
    """STRUCT_EXP : id llavea CONJEXP_STRUCT llavec"""
    p[0]=DecStructExp(idStruct=p[1],expStruct=p[3],line=p.lineno(1), column=0)
def p_conjexp_struct(p):
    """CONJEXP_STRUCT : CONJEXP_STRUCT coma EXSTRUCT"""
    p[1].append(p[3])
    p[0] = p[1]
def p_conjexp_struc_u(p):
    """CONJEXP_STRUCT : EXSTRUCT"""
    p[0] = [p[1]]
def p_exstruct(p):
    # Structname { var1:valor,var2:valor  }    expresion struct: var1 : valor
    """EXSTRUCT : id dospuntos EXPRESION
                | id dospuntos STRUCT_EXP """
    p[0]=ExpStruct(id=p[1],exp1=p[3],line=p.lineno(1), column=0)
    #{id:id expresion:expresion}
#Acceso struct
def p_acces_struct_expresion(p):
    """ACCESO_STRUCT  : id  punto  CONJ_ACCES"""
    p[0]=AccesStruct(idPrincipal=p[1],cIds=p[3],line=p.lineno(1), column=0)

#id.id.id ... id = val
def p_acces_struct_list(p):
    """CONJ_ACCES  : CONJ_ACCES punto id"""
    p[1].append(p[3])
    p[0]=p[1]
# id
def p_acces_struct(p):
    """CONJ_ACCES : id"""
    p[0]=[p[1]]
#modificacion de VARIABLES DECLARADAS COMO STRUCTS    id.val = hola
def p_mod_var_struct(p):
    """MOD_VAR_STRUCT : id punto CONJ_ACCES igual EXPRESION"""
    p[0]=ModiVarStruct(idPrincipal=p[1],cIds=p[3],exp=p[5],line=p.lineno(1), column=0)
#MODULOS
def p_modulos(p):
    """MODULO : modulo id llavea CONTENT_MOD llavec """
    p[0]=SaveModulo(id=p[2],cInst=p[4],line=p.lineno(1), column=0)
def p_content_mod_list(p):
    """CONTENT_MOD : CONTENT_MOD ELEMENT_MOD"""
    p[1].append(p[2])
    p[0]=p[1]
def p_content_mod_u(p):
    """CONTENT_MOD : ELEMENT_MOD"""
    p[0]=[p[1]]
def p_acces_inst_mod(p):
    """ELEMENT_MOD : pub INST_MOD
                | INST_MOD"""
    if p[1]!="pub":
        p[1].changeAcces(1)
        p[0]=p[1]
    else:
        p[0]=p[2]
def p_content_mod(p):
    """INST_MOD : FUNCION
                | MODULO
                | STRUCT
                | DECLARACION
                | DECARREGLO
                | DECVECTOR
                | DECSTRUCT
    """
    p[0]=p[1]
def p_acces_mod(p):
    """ACCESO_MOD : id dospuntos dospuntos CONJ_ACCES_MOD para CONJEXP parc
                | id dospuntos dospuntos CONJ_ACCES_MOD para parc"""
    if len(p)==8:
        p[0]=AccesModulo(id=p[1],cIds=p[4],Parametros=p[6],line=p.lineno(1), column=0)
    else:
        p[0] = AccesModulo(id=p[1], cIds=p[4], Parametros=[], line=p.lineno(1), column=0)
def p_conj_acces_mod1(p):
    """CONJ_ACCES_MOD : CONJ_ACCES_MOD dospuntos dospuntos id"""
    p[1].append(p[4])
    p[0]=p[1]
def p_conj_acces_mod2(p):
    """CONJ_ACCES_MOD : id"""
    p[0]=[p[1]]
# Error sintactico
def p_error(p):
    if p:
        print(f'Error de sintaxis simbolo: {p.value!r}  fila: {p.lineno} columna: {p.lexpos}')
    else:
        print("Syntax error")

# Build the parser
parser = yacc(debug=True)