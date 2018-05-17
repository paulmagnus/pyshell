################################################################################
#
# pyshell_translate.py
#
# The translator for the PyShell language. Takes in an abstract syntax tree
# and then translates the nodes of the tree into a Python3 executable. The
# translator also makes a linemap file that has a lookup table for conversion
# between the lines of the generated Python file and the original PyShell file.
#
# Written by Paul Magnus in Spring 2018
#
################################################################################

import sys
import re
import os
import pickle
import logging

from data_struct import ast
from pyshell_files import get_tmp_path, get_python_file, get_linemap_name, \
    remove_files

# Logging settings for DEBUGGING
# logging.basicConfig(level=logging.DEBUG, format='%(message)s')

# Line information for creation of the linemap file
line_num = 0
lines = {
    # python line : pyshell line
}

# Logging for debugging
log_tabs = ''

def log(function):
    """ This decorator logs when the process starts and ends. """
    def wrapper(*args, **kwargs):
        global log_tabs
        logging.debug(log_tabs + "Starting " + function.__name__)
        log_tabs += '  '
        result = function(*args, **kwargs)
        log_tabs = log_tabs[:-2] # Remove the two spaces
        logging.debug(log_tabs + "Ending " + function.__name__)
        return result
    return wrapper


################################################################################
# translate(parsetree:AST, filename:string)
# Translates the code from the parsetree to Python, writes the output to file.
################################################################################

def translate(parsetree, filename):

    # Determine the location of the given file
    # find_path = re.compile('(?P<p>[^/]+)/(?P<n>[^/]+).pysh')
    # found_path = find_path.search(filename)

    # global path
    # path = extract_base_directory(filename)
    # if found_path:
    #     filename = '.' + found_path.group('n') + '.py'
    #     path = found_path.group("p") + "/"
    # else:
    #     filename = '.' + filename[:-5] + '.py'
    #     path = ""

    # if path != "":
    #     # replace ./ in path if it exists
    #     if re.match(r"^\./.+$", path):
    #         # first character is a .
    #         # replace with current working directory (cwd)
    #         path = os.getcwd() + path[1:]
    #     elif re.match(r"^[^/].+$", path):
    #         path = os.getcwd() + "/" + path

    # Generate variable names
    generate_command_variables(parsetree)

    # TRANSLATE
    try:
        with open(get_python_file(filename), 'w+',
                  encoding='utf-8') as python_file:
            toPython(parsetree, python_file)
        export_map(filename)
    except IOError as e:
        print(e)
        print("Can't translate " + get_python_file(filename) +
              " due to IOError.", file = sys.stderr)
        remove_files(filename)
        sys.exit(1)

# This is the character that will be used for all PyShell specific variables
# so that we avoid collision with other Python variables
phi = '\u03C6'

# Generate a new PyShell specific variable
def generate_variable():
    var_name = phi + str(generate_variable.varnumber)
    generate_variable.varnumber += 1
    return var_name

generate_variable.varnumber = 0

def generate_command_variables(parsetree):
    for command in parsetree.flatten('COMMAND'):
        command.varname = generate_variable()

################################################################################
#
# Python conversion
#
################################################################################

def toPython(child, f, tabs=""):
    functions[child.label](child, f, tabs)

def advance(child):
    global line_num
    line_num += 1
    lines[line_num] = child.lineNum

def export_map(filename):
    with open(get_linemap_name(filename), 'wb') as f:
        pickle.dump(lines, f)

################################################################################
#
# Conversion functions
#
################################################################################

################################################################################
# PROGRAMFILE
# The program file incorporates the entire file
################################################################################

def c_PROGRAMFILE(child, f, tabs):
    # 0: shellblock

    f.write(tabs + 'import sys\n')
    advance(child)
    
    # add pyshell to the search path
    script_path = re.match(r'(?P<path>.*/)pyshell[^/]+',
                           os.path.realpath(__file__)).group('path')
    f.write(tabs + 'sys.path.append("' + script_path + '")\n')
    advance(child)

    f.write(tabs + 'import pyshell as ' + phi + '\n')
    advance(child)

    toPython(child[0], f, tabs)

    # End the file with a newline
    f.write('\n')


################################################################################
# EMPTY
# The empty rule allows for a rule to have an optional component
################################################################################
    
def c_EMPTY(child, f, tabs):
    pass


################################################################################
# PYTHON STRUCTURE
# These functions convert the general structure of a Python file
################################################################################

def c_BLOCK(child, f, tabs):
    # 0: statment_complex 1: nonempty_block
    toPython(child[0], f, tabs)
    if child[1].label != 'EMPTY':
        f.write('\n' + tabs)
    toPython(child[1], f, tabs)

def c_LINE(child, f, tabs):
    # 0: statement
    if child[0].label != 'SHELLBLOCK':
        for c in child.flatten('SHELLBLOCK'):
            toPython(c, f, tabs)

    toPython(child[0], f, tabs)

def c_STATEMENT_MULTI(child, f, tabs):
    # 0: statement1 1: other statemnets
    toPython(child[0], f, tabs)
    toPython(child[1], f, tabs)

def c_PYTHON(child, f, tabs):
    # 0: python code 1: further python code
    f.write(child[0])
    f.write(' ')
    toPython(child[1], f, tabs)

def c_SUITE_BLOCK(child, f, tabs):
    # 0: block
    f.write('    ')
    toPython(child[0], f, tabs+'    ')


################################################################################
#
# Shell constructs
#
################################################################################

################################################################################
# SHELLBLOCK
# This converts the container for shell script statements
################################################################################

def c_SHELLBLOCK(child, f, tabs):
    # 0: statement

    toPython(child[0], f, tabs)

    # Replace the shell block with the variable as Python code
    child.label = 'PYTHON'
    child.children = [child.varname, ast(None, 'EMPTY')]


################################################################################
# PROCESS
# These convert basic command processes
################################################################################

def c_PROC(child, f, tabs):
    # 0: command 1: procout

    toPython(child[0], f, tabs)

    if child[1].label != "EMPTY":
        toPython(child[1], f, tabs)

    child.parent.varname = child.varname

def c_COMMAND(child, f, tabs):
    # 0: command name 1: arglist

    child.parent.varname = child.varname
    
    f.write(child.varname + ' = ' + phi + ".Process(")
    toPython(child[0], f, tabs)
    if child[1].label != "EMPTY":
        f.write(", ")
        toPython(child[1], f, tabs)
    f.write(")\n" + tabs)

def c_ARGLIST(child, f, tabs):
    # 0: arg 1: arglist
    toPython(child[0], f, tabs)
    
    if child[1].label != "EMPTY":
        f.write(", ")
        toPython(child[1], f, tabs)

def c_ARG(child, f, tabs):
    # 0: argument
    toPython(child[0], f, tabs)


################################################################################
# FILE INTERACTION
# These translations deal with files
################################################################################

def c_PROCIN(child, f, tabs):
    # 0: command 1: instream 2: procout
    toPython(child[0], f, tabs)

    if child[0][0].label == 'VAR':
        # Create the stream if it does not already exist
        f.write('try:\n')
        f.write(tabs + '    ' + phi + phi + ' = ')
        toPython(child[1], f, tabs)
        f.write('\n' + tabs + 'except (UnboundLocalError, NameError):\n')
        f.write(tabs + '    ')
        toPython(child[1], f, tabs)
        f.write(' = ' + phi + '.Stream()\n' + tabs)

    f.write(child[0].varname + '.stdin = ')
    toPython(child[1], f, tabs)
    f.write('\n' + tabs)

    if child[2].label != 'EMPTY':
        toPython(child[2], f, tabs)

    child.parent.varname = child.varname

def c_STREAMOUT(child, f, tabs):
    # 0: stdout 1: stderr
    
    if child[0].label != 'EMPTY':

        if child[0][0].label == 'VAR':
            # Create the stream if it does not already exist
            f.write('try:\n')
            f.write(tabs + '    ' + phi + phi + ' = ')
            toPython(child[0], f, tabs)
            f.write('\n' + tabs + 'except (UnboundLocalError, NameError):\n')
            f.write(tabs + '    ')
            toPython(child[0], f, tabs)
            f.write(' = ' + phi + '.Stream()\n' + tabs)

        # Link the stream as stdout
        f.write(child.parent.varname + '.stdout = ')
        toPython(child[0], f, tabs)
        f.write('\n' + tabs)

    if child[1].label != 'EMPTY':

        if child[0][0].label == 'VAR':
            # Create the stream if it does not already exist
            f.write('try:\n')
            f.write(tabs + '    ' + phi + phi + ' = ')
            toPython(child[1], f, tabs)
            f.write('\n' + tabs + 'except (UnboundLocalError, NameError):\n')
            f.write(tabs + '    ')
            toPython(child[1], f, tabs)
            f.write(' = ' + phi + 'Stream()\n' + tabs)

        # Link the stream as stdout
        f.write(child.parent.varname + '.stderr = ')
        toPython(child[1], f, tabs)
        f.write('\n' + tabs)

def c_BOTHOUT(child, f, tabs):
    # 0: out file

    if child[0][0] == 'VAR':
        # Create the stream if it does not already exist
        f.write('try:\n')
        f.write(tabs + '    ' + phi + phi + ' = ')
        toPython(child[0], f, tabs)
        f.write('\n' + tabs + 'except (UnboundLocalError, NameError):\n')
        f.write(tabs + '    ')
        toPython(child[0], f, tabs)
        f.write(' = ' + phi + '.Stream()\n' + tabs)
    
    # Link the stream
    f.write(child.parent.varname + '.stdout = ')
    toPython(child[0], f, tabs)
    f.write('\n' + tabs)

    f.write(child.parent.varname + '.stderr = ' +
            child.parent.varname + '.stdout\n' + tabs)


################################################################################
# PIPES
# These are the conversions for pipes
################################################################################

def c_PIPE(child, f, tabs):
    # 0: stdout pipe target 1: stderr pipe target
    if child[0].label != 'EMPTY':
        toPython(child[0], f, tabs)
        f.write(child.parent.varname + '.stdout = ' + child[0].varname)
        f.write('\n' + tabs)

    if child[1].label != 'EMPTY':
        toPython(child[1], f, tabs)
        f.write(child.parent.varname + '.stderr = ' + child[1].varname)
        f.write('\n' + tabs)

def c_BOTHPIPE(child, f, tabs):
    # 0: out proc
    toPython(child[0], f, tabs)
    f.write(child.parent.varname + '.stdout = ' + child[0].varname + '\n')
    f.write(tabs + child.parent.varname + '.stderr = ' + 
            child.parent.varname + '.stdout\n' + tabs)
    


################################################################################
# Miscellaneous
################################################################################

def c_STRING(child, f, tabs):
    # 0: STRING
    f.write(child[0])

def c_VAR(child, f, tabs):
    # 0: VARNAME
    f.write(child[0])

def c_WORD(child, f, tabs):
    # 0: WORD
    f.write("'" + child[0] + "'")


################################################################################
# Translation lookup table
################################################################################

functions = {
    "PROGRAMFILE"        : c_PROGRAMFILE,
    "EMPTY"              : c_EMPTY,
    "BLOCK"              : c_BLOCK,
    "LINE"               : c_LINE,
    "STATEMENT_MULTI"    : c_STATEMENT_MULTI,
    "PYTHON"             : c_PYTHON,
    "SUITE_BLOCK"        : c_SUITE_BLOCK,
    "SHELLBLOCK"         : c_SHELLBLOCK,
    "PROC"               : c_PROC,
    "COMMAND"            : c_COMMAND,
    "ARGLIST"            : c_ARGLIST,
    "ARG"                : c_ARG,
    "PROCIN"             : c_PROCIN,
    "STREAMOUT"          : c_STREAMOUT,
    "BOTHOUT"            : c_BOTHOUT,
    "PIPE"               : c_PIPE,
    "BOHTPIPE"           : c_BOTHPIPE,
    "STRING"             : c_STRING,
    "VAR"                : c_VAR,
    "WORD"               : c_WORD,
}
