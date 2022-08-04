# Declaracion de tokens
from ply import lex

tokens = ('mas', 'menos', 'multi', 'div', 'para', 'parc', 'entero',"decimal","cadena","caracter","true","false")


# Caracteres ignorados
t_ignore = '[\t ]'


# Tokens con Regex
t_mas = r'\+'
t_menos = r'-'
t_multi = r'\*'
t_div = r'/'
t_mod = r'%'
t_para = r'\('
t_parc = r'\)'

#Simbolos relacionales
t_mayorigual=r'>='
t_menorigual=r'<='
t_igualigual=r'=='
t_diferente=r'!='
t_mayor=r'>'
t_menor=r'<'
t_igual=r'='
#simbolos logicos
t_or=r'||'
t_and=r'&&'
t_not=r'!'

#tipos de datos
t_i64=r'i64'
t_f64=r'f64'
t_bool= r'bool'
t_char=r'char'
t_string=r'&str|String'
#Palabras reservadas
t_struct=r'struct'
# Tipos de Datos, reconocer primero unos valores de otros para que los tokens funcione, en este caso decimal y entero, al reves reconoceria entero primero y daria error en el decimal
def t_decimal(t):
    r'\d+[.]\d+'
    t.value = float(t.value)
    return t
def t_entero(t):
    r'\d+'
    t.value = int(t.value)
    return t
def t_cadena(t):
    r'["](\\[\'\"\\nrt]|[^\n\"])*["]' 
    return t 
def t_caracter(t):
    r'[\'](\\[\'\"\\nrt]|[^\n\'])[\']' 
    return t 
def t_true(t):
    r'true'
    t.value=bool(t.value)
    return t
def t_false(t):
    r'false'
    t.value=bool(t.value)
    return t

#Ignora comentarios
def t_ignorar_comentarios(t):
    r'//.*'
    print("comentario")

# Ignora y hace una accion
def t_ignorar_salto(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Manejo de errores lexicos
def t_error(t):
    print(f'Caracter no reconocido {t.value[0]!r} en la linea {t.lexer.lineno}')
    t.lexer.skip(1)

lex.lex()