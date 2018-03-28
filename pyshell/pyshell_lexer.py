import sys
# import ply.lex as lex

# These are the lexing states. Each state controls which
# tokens are used.
states = (
    ('shell', 'exclusive'),
    ('code_block', 'inclusive'),
)

python_reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'for' : 'FOR',
    'while' : 'WHILE',
    'in' : 'IN',
}

tokens = list(python_reserved.values()) + [
    # BASIC TOKENS
    "PIPE",              # |
    "OUT",               # >
    # "IN",                # <
    "LPAREN",            # (
    "RPAREN",            # )
    "COMMA",             # ,
    "DELIMITER",

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

    "NL",
]

t_shell_PIPE = r'\|'
t_shell_OUT = r'>'
t_shell_IN = r'<'
t_shell_LPAREN = r'\('
t_shell_RPAREN = r'\)'
t_shell_COMMA = r','

t_shell_FILEOUT = r'\->'
t_shell_FILEAPPEND = r'>>'

t_shell_ERRPIPE = r'\!\|'
t_shell_BOTHPIPE = r'\&\|'
t_shell_ERROUT = r'\!>'
t_shell_BOTHOUT = r'\&>'

t_shell_WORD = r'[A-Za-z_\-\./\\]+'

t_NL = r'\n'

t_ignore_WS = r'[ \t]'
t_shell_ignore_WS = r'\s'

t_ANY_STRING = r'((?<!\\)\'.*?(?<!\\)\')|((?<!\\)\".*?(?<!\\)\")'

def t_DOCSTRING(t):
    r'((?<!\\)"""(?s).*?(?<!\\)""")|((?<!\\)\'\'\'(?s).*?(?<!\\)\'\'\')'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_DELIMITER(t):
    r'(?<!\\)\$'
    t.lexer.push_state('shell')
    return t

def t_shell_DELIMITER(t):
    r'(?<!\\)\$'
    t.lexer.pop_state()
    return t

def t_shell_VARNAME(t):
    r'@[a-zA-Z_][a-zA-Z0-9_]*'
    t.value = t.value[1:]
    return t

def t_pass_start(t):
    r'^([ \t]|\n|\#.*)+'
    t.lexer.lineno += t.value.count('\n')

def t_comment(t):
    r'\#.*'
    pass

def t_ANY_error(t):
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
