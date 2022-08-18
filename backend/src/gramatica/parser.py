from ply.yacc import yacc
from gramatica import lexer
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

from models.Ast.Ast import Ast

#Instrucciones
from models.Instruction.Println import Println
from models.Instruction.Declaracion import Declaracion
from models.Instruction.Asignacion import Asignacion
from models.Instruction.If import If
from  models.Instruction.Brazo import Brazo
from  models.Instruction.Match import Match
from  models.Instruction.Loop import Loop
from models.Instruction.Return import Return
from models.Instruction.Break import Break
from models.Instruction.Continue import Continue
from  models.Instruction.While import While
from models.Instruction.Funcion import Funcion
tokens = lexer.tokens

# EXPRESION : term MAS term
#            | term MENOS term
#            | term
# term : factor


# precedencia

precedence = (
    ('left', 'menos', 'mas'),
    ('left', 'multi', 'div'),
    ('right', 'UNARIO'),
)

def p_inicio(p):
    """
    INICIO : INSTRUCCIONES
    """
    p[0] = Ast(p[1])
    
def p_instrucciones_lista(p):
    """
    INSTRUCCIONES : INSTRUCCIONES INSTRUCCION puntoycoma
    """
    p[1].append(p[2])
    p[0] = p[1]
    
def p_instrucciones_instruccion(p):
    """
    INSTRUCCIONES : INSTRUCCION puntoycoma
    """
    p[0] = [p[1]]

def p_instruccion(p):
    """
    INSTRUCCION : PRINT
        | DECLARACION
        | ASIGNACION
        | IF
        | MATCH
        | CONTINUE
        | RETURN
        | BREAK
        | WHILE
        | EXPRESION
        | FUNCION
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
            |   pow para EXPRESION coma EXPRESION parc
    """
    # p contiene los elementos de la gramatica
    #
    # EXPRESION : term MAS term
    #   p[0]     : p[1] p[2] p[3]
    #
    if p[2] != '(':
        p[0] = Aritmeticas(exp1=p[1], operador=p[2], exp2=p[3], expU=False, linea=p.lineno(1), columna=0)
    else:
        p[0] = Aritmeticas(exp1=p[3], operador="pow", exp2=p[5], expU=False, linea=p.lineno(1), columna=0)

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
        | IF_TER
        | MATCH_TER
        | LOOP
        | CAST_AS
        | ABS
        | CLONE
        | SQRT
        | TO_STRING_OWNED
    """
    p[0]=p[1]
#CONJEXP=====================================================================================0
def p_cexp_list(p):
    """CONJEXP : CONJEXP coma EXPRESION"""
    p[1].append(p[3])
    p[0]=p[1]
def p_cexp(p):
    """CONJEXP : EXPRESION"""
    p[0] = [p[1]]
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
    EXPRESION : id
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
    """
    p[0] = p[1]
#If ternario=====================================================================================0
def p_if_ternario(p):
    """
    IF_TER : if  EXPRESION  llavea EXPRESION llavec
    """
    p[0] = If_ternario(exp=p[2],expB1=p[4],expB2="",line=p.lineno(1), column=0)
def p_if_else_ternario(p):
    """
    IF_TER : if  EXPRESION  llavea EXPRESION llavec else llavea EXPRESION llavec
    """
    p[0] = If_ternario(exp=p[2], expB1=p[4], expB2=p[8], line=p.lineno(1), column=0)
def p_if_else_if_ternario(p):
    """
    IF_TER : if EXPRESION  llavea EXPRESION llavec else IF_TER
    """
    p[0] = If_ternario(exp=p[2], expB1=p[4], expB2=p[7], line=p.lineno(1), column=0)
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
    """
    p[1].append(p[2])
    p[0] = p[1]
def p_brazosTer_brazo(p):
    """
    BRAZOS_TER : BRAZO_TER
    """
    p[0]=[p[1]]
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
#CLONE=====================================================================================
def p_clone(p):
    """CLONE : EXPRESION punto clone para parc"""
    p[0]=Clone(exp=p[1], line=p.lineno(1), column=0)
#Sqrt=====================================================================================
def p_sqrt(p):
    """SQRT : para CAST_AS parc punto sqrt para parc"""
    p[0] = Sqrt(exp=p[2], line=p.lineno(1), column=0)
#Sqrt=====================================================================================
def p_tostrig_owned(p):
    """TO_STRING_OWNED : EXPRESION punto toString para parc
        | EXPRESION punto toOwned para parc
    """
    p[0] = ToStringOwned(exp=p[1], line=p.lineno(1), column=0)
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
    """
    p[0] = Asignacion(p[1],p[3],linea=p.lineno(1), columna=0)

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
    MATCH : match EXPRESION llavea BRAZOS guionbajo igual mayor INSTRUCCION coma llavec
        |  match EXPRESION llavea guionbajo igual mayor INSTRUCCION coma llavec
    """
    if p[4]!="_":
        p[0] = Match(exp=p[2],lbrazos=p[4],default=[p[8]], line=p.lineno(1), column=0)
    else:
        p[0] = Match(exp=p[2], lbrazos=[], default=[p[8]], line=p.lineno(1), column=0)
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
        | CONJEXPM igual mayor INSTRUCCION coma
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
        p[0] = Declaracion(mut=False, id=p[1], tipo=p[3], exp=None, line=p.lineno(1), column=0)
    else:
        p[0]=Declaracion(mut=True,id=p[2],tipo=p[4],exp=None,line=p.lineno(1),column=0)

# Error sintactico
def p_error(p):
    print(f'Error de sintaxis {p.value!r}  fila: {p.lineno} columna: {p.lexpos}')


# Build the parser
parser = yacc(debug=True)