# Declaracion de tokens
from ply import lex

reservadas = {
    #r'exp regular' : id 
    'pow': 'pow',
    'struct': 'struct',
    'println!': 'println',
    'let':'let',
    'mut':'mut',
    'i64':'i64',
    'f64':'f64',
    'char': 'char',
    'bool':'bool',
    'String':'string',
    '&str': 'str',
    'if': 'if',
    'else': 'else'
}
tokens =['mas', 'menos', 'multi', 'div', 'para', 'parc', 'entero',"decimal","cadena","caracter","true","false",
          "mayor","menor","mayorigual","menorigual","igualigual","diferente",
          "or","and","not","interrogacion",
          'mod',
          'puntoycoma','dospuntos','llavea','llavec','cora','corc','igual','coma',
          'id'
          ] + list(reservadas.values())
        
        
# Caracteres ignorados
t_ignore = '[\t\r ]'



# Tokens con Regex
t_mas = r'\+'
t_menos = r'[-]'
t_multi = r'\*'
t_div = r'/'
t_mod = r'[%]'
t_para = r'\('
t_parc = r'\)'

#Simbolos relacionales
t_mayorigual=r'\>\='
t_menorigual=r'\<\='
t_igualigual=r'\=\='
t_diferente=r'\!\='
t_mayor=r'\>'
t_menor=r'\<'
t_igual=r'\='
#simbolos logicos
t_or=r'\|\|'
t_and=r'\&\&'
t_not=r'\!'

#otros simbolos
t_cora=r'\['
t_corc=r'\]'
t_llavea="\{"
t_llavec="\}"
t_coma=r'\,'
t_puntoycoma=r'\;'
t_dospuntos=r'\:'
t_interrogacion=r'\?'


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
    t.value=True
    return t
def t_false(t):
    r'false'
    t.value=False
    return t
def t_println(t):
    r"""println!"""
    t.type=reservadas.get(t.value)
    return t
def t_str(t):
    r""" \&str"""
    t.type = reservadas.get(t.value)
    return t

def t_id(t):
    r'[A-Za-z_ñÑ][A-Za-z0-9_ñÑ]*'
    t.type =reservadas.get(t.value, 'id')
    return t 

#Ignora comentarios
def t_ignorar_comentarios(t):
    r'\/\/.*'

# Ignora y hace una accion
def t_ignorar_salto(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Manejo de errores lexicos
def t_error(t):
    print(f'Caracter no reconocido {t.value[0]!r} en la linea {t.lexer.lineno}')
    t.lexer.skip(1)

lex.lex()