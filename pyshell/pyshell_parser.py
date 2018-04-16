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
start = "programfile"

def p_programfile(p):
    '''programfile : nonempty_block
                   | empty'''
    p[0] = ast(p, "PROGRAMFILE", 1)

def p_nonempty_block(p):
    '''nonempty_block : statement_complex empty
                      | statement_complex nonempty_block'''
    p[0] = ast(p, "BLOCK", 1, 2)

def p_statement_complex(p):
    '''statement_complex : suite
                         | line NL'''
    p[0] = p[1]

def p_line(p):
    '''line : statement_multi
            | statement_shell'''
    p[0] = ast(p, "LINE", 1)

def p_statement_single(p):
    '''statement_multi : shellblock
                       | python_code'''
    p[0] = p[1]
    # p[0] = ast(p, "STATEMENT_SINGLE", 1)

def p_statement_multi(p):
    '''statement_multi : python_code statement_shell'''
    p[0] = ast(p, "STATEMENT_MULTI", 1, 2)

def p_statement_shell(p):
    '''statement_shell : shellblock statement_multi'''
    p[0] = ast(p, "STATEMENT_MULTI", 1, 2)

def p_python_code(p):
    '''python_code : PYTHON opt_python
                   | STRING opt_python
                   | DOCSTRING opt_python'''
    p[0] = ast(p, "PYTHON", 1, 2)

def p_opt_python(p):
    '''opt_python : python_code
                  | empty'''
    p[0] = p[1]

def p_suite_block(p):
    '''suite : INDENT nonempty_block DEDENT'''
    p[0] = ast(p, "SUITE_BLOCK", 2)

def p_shellblock(p):
    '''shellblock : SHELL_DELIMITER proc SHELL_DELIMITER
                  | SHELL_DELIMITER procin SHELL_DELIMITER'''
    p[0] = ast(p, "SHELLBLOCK", 2)

def p_empty(p):
    '''empty : %prec EPSILON'''
    p[0] = ast(p, "EMPTY")

def p_procin(p):
    '''procin : command STREAM_IN instream procout
              | command STREAM_IN instream empty'''
    p[0] = ast(p, "PROCIN", 1, 3, 4)

def p_proc(p):
    '''proc : command empty
            | command procout'''
    p[0] = ast(p, "PROC", 1, 2)

def p_command(p):
    '''command : WORD arglist
               | WORD empty'''
    p[0] = ast(p, "COMMAND", 1, 2)

def p_arglist(p):
    '''arglist : arg empty
               | arg arglist'''
    p[0] = ast(p, "ARGLIST", 1, 2)

def p_arg(p):
    '''arg : WORD
           | var
           | STRING'''
    p[0] = ast(p, "ARG", 1)

def p_procout(p):
    '''procout : pipeout
               | streamout
               | fileout'''
    p[0] = p[1]
    # p[0] = ast(p, "PROCOUT", 1)

def p_pipe(p):
    '''pipeout : PIPE empty proc empty empty empty
               | PIPE LPAREN proc COMMA proc RPAREN
               | ERRPIPE empty empty empty proc empty'''
    p[0] = ast(p, "PIPE", 3, 5)

def p_bothpipe(p):
    '''pipeout : BOTHPIPE proc'''
    p[0] = ast(p, "BOTHPIPE", 2)

def p_streamout(p):
    '''streamout : STREAM_OUT empty var empty empty empty
                 | STREAM_OUT LPAREN var COMMA var RPAREN
                 | ERROUT empty empty empty var empty'''
    p[0] = ast(p, "STREAMOUT", 3, 5)

def p_streamout_both(p):
    '''streamout : BOTHOUT VARNAME'''
    p[0] = ast(p, "BOTHOUT", 2)

def p_fileout(p):
    '''fileout : FILEOUT file'''
    p[0] = ast(p, "FILEOUT", 2)

def p_file_append(p):
    '''fileout : FILEAPPEND file'''
    p[0] = ast(p, "FILEAPPEND", 2)

def p_instream(p):
    '''instream : WORD
                | var
                | STRING'''
    p[0] = p[1]
    # p[0] = ast(p, "INSTREAM", 1)

def p_file(p):
    '''file : WORD
            | var
            | STRING'''
    p[0] = ast(p, "FILE", 1)

def p_var(p):
    '''var : VARNAME'''
    p[0] = ast(p, "VAR", 1)

def p_error(p):
    # Invalid character - Lexer takes care of this error
    print('p =',p)
    if not p:
        # TODO: Remove this print statement when done debugging
        print("Debugging: Invalid character")
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

    if p.type == 'DEDENT' or p.type == 'INDENT':
        error_length = p.value
    else:
        error_length = len(p.value)

    # Find the column of the token in the source code
    if p.type == 'NL':
        col = len(line) + 1
    elif p.type == 'INDENT' or p.type == 'DEDENT':
        col = 1
    else:
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

    if p.type == 'DEDENT' or p.type == 'INDENT':
        print('IndentationError: outer indentation and unindentation do '
              'not match\n', file=sys.stderr)

    if p.type == 'NL':
        print('Unexpected new line.', file=sys.stderr)
        
    exit(1)
