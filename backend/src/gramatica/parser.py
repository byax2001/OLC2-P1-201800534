from ply.yacc import yacc
from gramatica import lexer

from models.Expresion.Operacion.Aritmeticas import Aritmeticas
from models.Expresion.Primitivo import Primitivo
from models.Expresion.Id import Id
from models.Ast.Ast import Ast

#Instrucciones
from models.Instruction.println import Println


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
    INSTRUCCIONES : INSTRUCCIONES INSTRUCCION
    """
    p[0] = p[1].append(p[2])
    
def p_instrucciones_instruccion(p):
    """
    INSTRUCCIONES : INSTRUCCION
    """
    p[0] = [p[1]]

def p_instruccion(p):
    """
    INSTRUCCION : PRINT puntoycoma
    """
    p[0] = p[1]

def p_expresion(p):
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

def p_EXPRESION_par(p):
    """
    EXPRESION : para EXPRESION parc
    """
    p[0] = p[2]


def p_factor_unario(p):
    """
    EXPRESION : menos EXPRESION %prec UNARIO
    """
    p[0] = Aritmeticas(exp1=p[2], operador=p[1], exp2=None, expU=True, linea=p.lineno(1), columna=0)
        
def p_exp_tdato(p):
    """
    EXPRESION : TIPODATO
    """
    p[0]=p[1]
    
def p_tipo_dato(p):
    """
    TIPODATO : entero
        | decimal
        | cadena
        | caracter 
    """
    p[0] = Primitivo(p[1], p.lineno(1), 0) 
def p_id(p):
    """
    EXPRESION : id
    """  
    p[0] = p[1]
#Instrucciones
def p_println(p):
    """
    PRINT : println para EXPRESION parc
    """
    p[0] = Println(p[3], p.lineno(1), 0)

# Error sintactico
def p_error(p):
    print(f'Error de sintaxis {p.value!r}')


# Build the parser
parser = yacc()