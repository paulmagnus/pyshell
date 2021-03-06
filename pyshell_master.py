################################################################################
#
# pyshell_master.py
#
# This file contains the main program for translation and exection of PyShell
# programs.
#
# Written by Paul Magnus in Spring 2018
#
################################################################################


# PYTHON MODULES
import ply.lex as lex
import ply.yacc as yacc
import sys
import os

# LOCAL FILES
from pyshell_lexer import *
from pyshell_parser import *
from pyshell_translate import translate
from pyshell_files import get_tmp_path
from pyshell_run import run

yacc.error_count = 3

def usage():
    ''' Prints out how to use the pyshell system. '''

    print("Error: The PyShell translator takes one argument - the name of the "
          "file to be translated.", file=sys.stderr)
    sys.exit(1)

def find_column(input, token):
    ''' Compute the column for a token, in the context of some input. '''

    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    return token.lexpos - last_cr

def get_line_numbers(p, n):
    ''' Returns a list of line numbers for the n statements in p. '''
    return [p.lineno(i) for i in range(n)]

def parse_file(filename):
    ''' Builds the parser for the PyShell language from lexer and parser
    filese and then returns the abstract syntax parse tree for the file.'''
    
    if not os.path.isfile(filename):
        print("Error:", filename, "could not be found", file=sys.stderr)
        sys.exit(1)

    with open(filename, 'rU') as pyshellfile:
        lexer = lex.lex()
        lexer.indentwidth = None
        lexer.indentedline = None
        lexer.indentstack = [0]
        lexer.input(pyshellfile.read() + '\n')
        
        parser = yacc.yacc()
        lexer.parser = parser
        parsetree = parser.parse(tracking = True,
                                 # debug=True
        )
        
        return parsetree

def main():

    # Check args
    if len(sys.argv) != 2:
        usage()

    # Confirm that the file is valid
    filename = sys.argv[1]

    # if len(filename) < 6 or filename[-5:] != ".pysh":
    #     print("Error: file must be a pysh file.\n"
    #           "File given: '" + filename + "'", file=sys.stderr)
    #     sys.exit(1)

    # Process and execute
    parsetree = parse_file(filename)
    
    # print("Parsetree---------------------------")
    # print(parsetree)
    # print("------------------------------------")
    
    if not parsetree:
        print('Parse failed')
    else:
        try:
            os.stat(get_tmp_path())
        except:
            os.mkdir(get_tmp_path())
        
        translate(parsetree, filename)
        run(filename)

if __name__ == "__main__":
    main()

# Notes:
# Do we handle Python errors like in cspy?
