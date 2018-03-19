import sys
import ply.lex as lex

tokens = [
    # BASIC TOKENS
    "VARID",        # @
    "PIPE",         # |
    "OUT",          # >
    "IN",           # <
    "LPAREN",       # (
    "RPAREN",       # )
    "COMMA",        # ,

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

t_VARID = r'@'
t_PIPE = r'\|'
t_OUT = r'>'
t_IN = r'<'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','

t_FILEOUT = r'\->'
t_FILEAPPEND = r'>>'

t_ERRPIPE = r'\!\|'
t_BOTHPIPE = r'\&\|'
t_ERROUT = r'\!>'
t_BOTHOUT = r'\&>'

t_STRING = r'(\"(\\.|[^"\n\r\f\v])*\")|(\'(\\.|[^\'\n\r\f\v])*\')'
t_WORD = r'[^\s\'\"@><\|\(\),\!]+'
t_ignore_WS = r'[ \t]'

def t_VARNAME(t):
    r'@[a-zA-Z_][a-zA-Z0-9_]*'
    t.value = t.value[1:]
    return t

def t_error(t):
    print("pyshell : Syntax Error", file=sys.stderr)
    # TODO: Continue possibly based on the t_error in cspy_lexer.py

lex.lex()
