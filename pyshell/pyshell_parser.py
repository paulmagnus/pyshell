import re, sys
import ply.yacc as yacc
import pyshell_lexer
tokens = pyshell_lexer.tokens

# Note: The rules for the context-free grammar are defined in the docstring
# of each function. Changing these docstrings will change how this operates.

# Start rule
start = "statement"

def opt_arg(p, num):
    return p[num] if len(p) > num else None

def p_statement(p):
    '''statement : procin
                 | proc'''
    p[0] = ("STATEMENT", p[1])

def p_command(p):
    '''command : WORD'''
    p[0] = ("COMMAND", [p[1]])

def p_command_list(p):
    '''command : WORD arglist'''
    p[0] = ("COMMAND", [p[1]] + list(p[2]))

def p_arglist(p):
    '''arglist : WORD arglist
               | var arglist
               | STRING arglist'''
    p[0] = (p[1],) + p[2]

def p_arg(p):
    '''arglist : WORD
               | var
               | STRING'''
    p[0] = (p[1],)

def p_proc(p):
    '''proc : command
            | command procout'''
    p[0] = ("PROC", p[1], opt_arg(p, 2))

def p_procin(p):
    '''procin : command IN streamlist
              | command IN streamlist procout'''
    p[0] = ("PROCIN", p[1], p[3], opt_arg(p, 4))

def p_streamlist(p):
    '''streamlist : var
                  | STRING
                  | WORD'''
    p[0] = ("STREAMLIST", p[1])

def p_file(p):
    '''file : WORD
            | STRING
            | var'''
    p[0] = ("FILE", p[1])

def p_procout(p):
    '''procout : pipeout
               | streamout
               | fileout'''
    p[0] = ("PROCOUT", p[1])

def p_pipe(p):
    '''pipeout : PIPE proc'''
    p[0] = ("PIPE", p[2], None)

def p_pipesplit(p):
    '''pipeout : PIPE LPAREN proc COMMA proc RPAREN'''
    p[0] = ("PIPE", p[3], p[5])

def p_pipedup(p):
    '''pipeout : BOTHPIPE proc'''
    p[0] = ("PIPE", p[3], p[3])

def p_pipeerr(p):
    '''pipeout : ERRPIPE proc'''
    p[0] = ("PIPE", None, p[2])

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

def p_var(p):
    '''var : VARNAME'''
    p[0] = ("VAR", p[1])

def p_error(p):
    print("Error!")

yacc.yacc()

parsed = yacc.parse('ls -a -l "my_folder" < @a !| grep @search')
print(parsed)
