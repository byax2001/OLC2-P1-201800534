from ply.yacc import yacc
from gramatica import lexer
#Expresiones
from models.Expresion.Operacion.Aritmeticas import Aritmeticas
from models.Expresion.Operacion.Relacionales import Relacionales
from models.Expresion.Operacion.Logicas import Logicas
from models.Expresion.Primitivo import Primitivo
from models.Expresion.Id import Id
from models.Expresion.If_Ternario import If_ternario
from models.Ast.Ast import Ast

#Instrucciones
from models.Instruction.println import Println
from models.Instruction.Declaracion import Declaracion
from models.Instruction.Asignacion import Asignacion
from models.Instruction.If import If
from  models.Instruction.Brazo import Brazo
from  models.Instruction.Match import Match

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
    """
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
#PRODUCCION PARA EXPRESIONES DE UN SOLO ELEMETO
def p_exp_one_element(p):
    """
    EXPRESION : TIPODATO
        | IF_TER
    """
    p[0]=p[1]
#tipo de dato
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
#tipo de variable
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
#If ternario
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

#Instrucciones
def p_println(p):
    """
    PRINT : println para EXPRESION parc
    """
    p[0] = Println(p[3], p.lineno(1), 0)
#Declaraciones
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
#Asignaciones
def p_asignaciones(p):
    """
    ASIGNACION : id igual EXPRESION
    """
    p[0] = Asignacion(p[1],p[3],linea=p.lineno(1), columna=0)

#If
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

#match
def p_match_1(p):
    """
    MATCH : match EXPRESION llavea BRAZOS guionbajo igual mayor BLOQUE_INST llavec
    """
    p[0] = Match(exp=p[2],lbrazos=p[4],default=p[8], line=p.lineno(1), column=0)
def p_match_2(p):
    """
    MATCH : match EXPRESION llavea BRAZOS guionbajo igual mayor INSTRUCCION coma llavec
    """
    p[0] = Match(exp=p[2],lbrazos=p[4],default=[p[8]], line=p.lineno(1), column=0)
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
    BRAZO : CONJEXP igual mayor BLOQUE_INST
        | CONJEXP igual mayor INSTRUCCION coma
    """
    if type(p[4]) in (tuple,list):
        p[0] = Brazo(cExp=p[1],bloque=p[4], line=p.lineno(1), column=0)
    else:
        p[0] = Brazo(cExp=p[1], bloque=[p[4]], line=p.lineno(1), column=0)
def p_conj_exp_match_list(p):
    """CONJEXP : CONJEXP bvertical EXPRESION"""
    p[1].append(p[3])
    p[0]=p[1]
def p_conj_exp_match_exp(p):
#bloque instrucciones
    """CONJEXP : EXPRESION"""
    p[0]=[p[1]]
def p_bloque_instrucciones(p):
    """
    BLOQUE_INST : llavea  INSTRUCCIONES llavec
    """
    p[0]=p[2]
# Error sintactico
def p_error(p):
    print(f'Error de sintaxis {p.value!r} ')


# Build the parser
parser = yacc()