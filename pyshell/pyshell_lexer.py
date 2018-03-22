import sys
# import ply.lex as lex

tokens = [
    # BASIC TOKENS
    "PIPE",         # |
    "OUT",          # >
    "IN",           # <
    "LPAREN",       # (
    "RPAREN",       # )
    "COMMA",        # ,
    "DELIMITER",    # $
    "NL",           # \n

    # COMPLEX TOKENS
    "FILEOUT",      # ->
    "FILEAPPEND",   # >>
    "ERRPIPE",      # !|
    "BOTHPIPE",     # &|
    "ERROUT",       # !>
    "BOTHOUT",      # &>

    # MISC
    "VARNAME",      # Python variable name
    "STRING",       # Python string
    "WORD",         # Bash word
]

t_PIPE = r'\|'
t_OUT = r'>'
t_IN = r'<'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_DELIMITER = r'\$'
t_NL = r'\n'

t_FILEOUT = r'\->'
t_FILEAPPEND = r'>>'

t_ERRPIPE = r'\!\|'
t_BOTHPIPE = r'\&\|'
t_ERROUT = r'\!>'
t_BOTHOUT = r'\&>'

t_STRING = r'(\"(\\.|[^"\n\r\f\v])*\")|(\'(\\.|[^\'\n\r\f\v])*\')'
t_WORD = r'[^\s\'\"@><\|\(\),\!\$\&]+'
t_ignore_WS = r'[ \t]'

def t_VARNAME(t):
    r'@[a-zA-Z_][a-zA-Z0-9_]*'
    t.value = t.value[1:]
    return t

def t_pass_start(t):
    r'^([ \t]|\n|\#.*)+'
    t.lexer.lineno += t.value.count('\n')

def t_comment(t):
    r'\#.*'
    t.lexer.lineno += t.value.count('\n')
    pass

def t_error(t):
    print("pyshell : Syntax Error", file=sys.stderr)
    
    # Get the line from the source text
    source = t.lexer.lexdata.split('\n')
    line = source[t.lineno - 1]

    # Find the column of the token in the source code
    last_nl = t.lexer.lexdata.rfind('\n', 0, t.lexpos)
    if last_nl < 0:
        last_nl = -1
    next_nl = t.lexer.lexdata.find('\n', t.lexpos + len(t.value),
                                   len(t.lexer.lexdata))
    
    if next_nl < 0:
        next_nl = len(t.lexer.lexdata)
    col = t.lexpos - last_nl

    # Display line information
    message = "Line " + str(t.lineno) + ", Column " + str(col) + "\n\n" + \
              line + "\n" + " " * (col - 1) + "^"
    print(message, file=sys.stderr)

    # Display error message
    result = "Illegal character "
    if (ord(t.value[0]) >= 32 or ord(t.value[0]) <= 126):
        result += "'" + t.value[0] + "'"
    else:
        result += "#" + ord(t.value[0])
    print(result, file=sys.stderr)

    t.lexer.skip(len(t.value))

# lexer = lex.lex()
