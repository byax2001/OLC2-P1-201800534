from ply.yacc import yacc
from gramatica import lexer

tokens = lexer.tokens

# expression : term MAS term
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
    p[0] = p[1]
    
def p_instrucciones(p):
    """
    INICIO : INSTRUCCIONES INSTRUCCION
        | INSTRUCCION
    """
    p[0] = p[1]

def p_instruccion(p):
    """
    INSTRUCCION: EXPRESION
    """
    p[0] = p[1]

def p_expresion(p):
    """
    EXPRESION :  EXPRESION mas EXPRESION 
            |   EXPRESION menos EXPRESION
            |   EXPRESION div EXPRESION
            |   EXPRESION multi EXPRESION
            |   EXPRESION mod EXPRESION
            
            |      
    """
    # p contiene los elementos de la gramatica
    #
    # expression : term MAS term
    #   p[0]     : p[1] p[2] p[3]
    #
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_par(p):
    """
    expression : PARA expression PARC
    """
    p[0] = p[2]



def p_factor_number(p):
    """
    expression : ENTERO
        | DECIMAL
    """
    p[0] = p[1]


def p_factor_unario(p):
    """
    expression : MAS expression
           | MENOS expression %prec UNARIO
    """
    if p[1] == '-':
        p[0] = -p[2]
    else:
        p[0] = p[2]
        


# Error sintactico
def p_error(p):
    print(f'Error de sintaxis {p.value!r}')


# Build the parser
parser = yacc()