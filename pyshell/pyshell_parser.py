import re, sys
import ply.yacc as yacc
import pyshell_lexer
from data_struct import ast

tokens = pyshell_lexer.tokens

# Note: The rules for the context-free grammar are defined in the docstring
# of each function. Changing these docstrings will change how this operates.

precedence = (
    ('nonassoc', 'EPSILON'),
)

# Start rule
start = "shellblock"

def opt_arg(p, num):
    return p[num] if len(p) > num else None

def p_shellblock(p):
    '''shellblock : DELIMITER statement DELIMITER NL'''
    p[0] = ast(p, "SHELLBLOCK", 2)

def p_empty(p):
    '''empty : %prec EPSILON'''
    pass

def p_statement(p):
    '''statement : proc
                 | procin'''
    p[0] = ast(p, "STATEMENT", 1)

def p_procin(p):
    '''procin : command IN instream procout
              | command IN instream empty'''
    p[0] = ast(p, "PROCIN", 1, 3, 4)

def p_proc(p):
    '''proc : command empty
            | command procout'''
    p[0] = ast(p, "PROC", 1, 2)

def p_command(p):
    '''command : WORD arglist'''
    p[0] = ast(p, "COMMAND", 1, 2)

def p_arglist(p):
    '''arglist : nonempty_arglist
               | empty'''
    p[0] = ast(p, "ARGLIST", 1)

def p_arglist_single(p):
    '''nonempty_arglist : arg'''
    p[0] = ast(p, "ARGLIST_SINGLE", 1)

def p_arglist_multi(p):
    '''nonempty_arglist : arg nonempty_arglist'''
    p[0] = ast(p, "ARGLIST_MULTI", 1, 2)

def p_arg(p):
    '''arg : WORD
           | var
           | STRING'''
    p[0] = ast(p, "ARG", 1)

def p_procout(p):
    '''procout : pipeout
               | streamout
               | fileout'''
    p[0] = ast(p, "PROCOUT", 1)

def p_pipe(p):
    '''pipeout : PIPE empty proc empty empty empty
               | PIPE LPAREN proc COMMA proc RPAREN
               | ERRPIPE empty empty empty proc empty'''
    p[0] = ast(p, "PIPE", 3, 5)

def p_bothpipe(p):
    '''pipeout : BOTHPIPE proc'''
    p[0] = ast(p, "BOTHPIPE", 2)

def p_streamout(p):
    '''streamout : OUT VARNAME
                 | OUT LPAREN VARNAME COMMA VARNAME RPAREN
                 | ERROUT VARNAME
                 | BOTHOUT VARNAME'''
    pass

def p_fileout(p):
    '''fileout : FILEOUT file
               | FILEAPPEND file'''
    pass

def p_instream(p):
    '''instream : WORD
                | var
                | STRING'''
    p[0] = ast(p, "INSTREAM", 1)

def p_file(p):
    '''file : WORD
            | var
            | STRING'''
    p[0] = ast(p, "STREAMLIST", 1)

def p_var(p):
    '''var : VARNAME'''
    p[0] = ast(p, "VAR", 1)

def p_error(p):
    # Invalid character - Lexer takes care of this error
    if not p:
        return

    print("pyshell : Syntax Error", file=sys.stderr)

    # Get the line from the source code
    source = p.lexer.lexdata.split('\n')
    lineno = p.lineno
    line = source[lineno - 1]

    # Assume error occurred on previous line if current line is whitespace
    # Find previous nonwhitespace or noncomment line
    white_space = re.compile('^([ \t]+|[#].*)$')
    while (white_space.match(line) or line == '') and lineno != 1:
        lineno = lineno - 1
        line = source[lineno - 1]

    error_length = len(p.value)

    # Find the column of the token in the source code
    last_nl = p.lexer.lexdata.rfind('\n', 0 , p.lexpos)
    if last_nl < 0:
        last_nl = -1
    
    next_nl = p.lexer.lexdata.find('\n', p.lexpos + error_length,
                                   len(p.lexer.lexdata))
    if next_nl < 0:
        next_nl = len(p.lexer.lexdata)
    col = p.lexpos - last_nl

    message = "Line " + str(lineno) + ", Column " + str(col) + "\n\n" + \
              line + "\n" + " " * (col - 1) + "^" * (error_length)
    print(message, file=sys.stderr)

parser = yacc.yacc()
