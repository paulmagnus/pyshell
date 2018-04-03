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
    '''statement_complex : loop
                         | conditional
                         | statement_multi NL
                         | statement_multi SEMICOLON NL'''
    p[0] = p[1]

def p_statement_multi(p):
    '''statement_multi : statement_multi SEMICOLON statement_multi'''
    p[0] = ast(p, "STATEMENT_MULTI", 1, 3)

def p_statement_single(p):
    '''statement_multi : statement_simple'''
    p[0] = p[1]
    
def p_statement_simple(p):
    '''statement_simple : statement_result
                        | statement_no_result'''
    p[0] = p[1]

def p_statement_result(p):
    '''statement_result : assignment
                        | return
                        | assert
                        | yield'''
    p[0] = ast(p, "STATEMENT_RESULT", 1)

def p_statement_no_result(p):
    '''statement_no_result : shellblock
                           | python_code'''
    p[0] = ast(p, "STATEMENT_NO_RESULT", 1)

# LOOPS
def p_loop(p):
    '''loop : while_loop
            | for_loop'''
    p[0] = p[1]

def p_while(p):
    '''while_loop : WHILE expression COLON suite'''
    p[0] = ast(p, "WHILELOOP", 2, 4)

def p_for(p):
    '''for_loop : FOR PYTHON IN expression COLON suite'''
    p[0] = ast(p, "FORLOOP", 2, 4, 6)

# Conditionals
def p_conditional(p):
    '''conditional : IF expression COLON suite conditional_extension
                   | IF expression COLON suite empty'''
    p[0] = ast(p, "CONDITIONAL", 2, 4, 5)

def p_conditional_extension_elif(p):
    '''conditional_extension : ELIF expression COLON suite conditional_extension'''
    p[0] = ast(p, "CONDITIONAL_ELIF", 2, 4, 5)

def p_conditional_extension_else(p):
    '''conditional_extension : ELSE COLON suite'''
    p[0] = ast(p, "CONDITIONAL_ELSE", 3)

# ASSIGNMENT
def p_assignment(p):
    '''assignment : python_code ASSIGNMENT_OPERATOR expression'''
    p[0] = ast(p, "ASSIGNMENT", 1, 2, 3)

def p_return(p):
    '''return : RETURN empty
              | RETURN expression'''
    p[0] = ast(p, "RETURN", 2)

def p_assert(p):
    '''assert : ASSERT expression'''
    p[0] = ast(p, "ASSERT", 2)

def p_yield(p):
    '''yield : YIELD expression'''
    p[0] = ast(p, "YIELD", 2)

def p_expression(p):
    '''expression : shellblock
                  | python_code'''
    p[0] = p[1]

def p_python_code(p):
    '''python_code : PYTHON python_code
                   | STRING python_code
                   | DOCSTRING python_code
                   | PYTHON empty
                   | STRING empty
                   | DOCSTRING empty'''
    p[0] = ast(p, "PYTHON", 1, 2)

def p_suite_block(p):
    '''suite : NL INDENT nonempty_block DEDENT'''
    p[0] = ast(p, "SUITE_BLOCK", 3, 4)

def p_suite_inline(p):
    '''suite : statement_simple NL'''
    p[0] = ast(p, "SUITE_INLINE", 1)
    
def p_shellblock(p):
    '''shellblock : SHELL_DELIMITER statement SHELL_DELIMITER'''
    p[0] = ast(p, "SHELLBLOCK", 2)

def p_empty(p):
    '''empty : %prec EPSILON'''
    p[0] = ast(p, "EMPTY")

def p_statement(p):
    '''statement : proc
                 | procin'''
    p[0] = ast(p, "STATEMENT", 1)

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
    '''streamout : STREAM_OUT VARNAME
                 | STREAM_OUT LPAREN VARNAME COMMA VARNAME RPAREN
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
    print('p =',p)
    if not p:
        print("Invalid character")
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
