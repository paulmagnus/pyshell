import sys
import ply.yacc as yacc
from test_lexer import tokens

precedence = (
    ("nonassoc", "EPSILON"),
)

start = "file"

def p_empty(p):
    '''empty : %prec EPSILON'''
    p[0] = ("EMPTY",)

def p_file(p):
    '''file : lines'''
    p[0] = ("FILE", p[1])

def p_lines(p):
    '''lines : line lines
             | line empty'''
    p[0] = ("LINES", p[1]) + tuple(p[2][1:])

def p_line(p):
    '''line : code NL'''
    p[0] = ("LINE", p[1])

def p_code(p):
    '''code : CODE empty
            | shell empty
            | CODE code
            | shell code'''
    p[0] = ("CODE", p[1]) + tuple(p[2][1:])

def p_shell(p):
    '''shell : SHELL_DELIMITER CODE SHELL_DELIMITER'''
    p[0] = ("SHELL", p[2])

def p_error(p):
    print("Error!", file=sys.stderr)

yacc.yacc()

parsed = yacc.parse('''for i in $ls$:
    print(i)
''')
print(parsed)