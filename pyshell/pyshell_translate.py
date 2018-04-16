import sys, re, os, pickle, logging
from data_struct import ast

logging.basicConfig(level=logging.DEBUG,
                    format='%(message)s')

tmp_path = './'
line_num = 0
lines = {
    # python line : pyshell line
}

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

def translate(parsetree, filename):

    find_path = re.compile('(?P<p>[^/]+)/(?P<n>[^/]+).pysh')
    found_path = find_path.search(filename)

    global path
    if found_path:
        filename = '.' + found_path.group('n') + '.py'
        path = found_path.group("p") + "/"
    else:
        filename = '.' + filename[:-5] + '.py'
        path = ""

    if path != "":
        # replace ./ in path if it exists
        if re.match(r"^\./.+$", path):
            # first character is a .
            # replace with current working directory (cwd)
            path = os.getcwd() + path[1:]
        elif re.match(r"^[^/].+$", path):
            path = os.getcwd() + "/" + path

    # Generate variable names
    generate_command_variables(parsetree)

    # TRANSLATE
    try:
        with open(tmp_path + filename, 'w+', encoding='utf-8') as python_file:
            toPython(parsetree, python_file)
        export_map(filename)
    except IOError:
        print("Can't translate " + tmp_path + filename + " due to IOError.",
              file = sys.stderr)
        remove_files()
        sys.exit(1)

phi = '\u03C6'

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
    filename = filename[:-3] + "_linemap"
    with open(tmp_path + filename, 'wb') as f:
        pickle.dump(lines, f)

################################################################################
#
# Conversion functions
#
################################################################################

def c_EMPTY(child, f, tabs):
    pass

################################################################################
#
# Python constructs
#
################################################################################

def c_PROGRAMFILE(child, f, tabs):
    # 0: shellblock

    f.write(tabs + 'import sys\n')
    advance(child)
    
    # add pyshell to the search path
    script_path = re.match(r'(?P<path>.*/)[^/]+',
                           os.path.realpath(__file__)).group('path')
    f.write(tabs + 'sys.path.append("' + script_path + '")\n')
    advance(child)

    f.write(tabs + 'import process as ' + phi + '\n')
    advance(child)

    toPython(child[0], f, tabs)

    # End the file with a newline
    f.write('\n')

def c_BLOCK(child, f, tabs):
    # 0: statment_complex 1: nonempty_block
    toPython(child[0], f, tabs)
    if child[1].label != 'EMPTY':
        f.write('\n' + tabs)
    toPython(child[1], f, tabs)

def c_SUITE_BLOCK(child, f, tabs):
    # 0: block
    f.write('    ')
    toPython(child[0], f, tabs+'    ')

def c_PYTHON(child, f, tabs):
    # 0: python code 1: further python code
    f.write(child[0])
    f.write(' ')
    toPython(child[1], f, tabs)

def c_STATEMENT_MULTI(child, f, tabs):
    # 0: statement1 1: other statemnets
    toPython(child[0], f, tabs)
    toPython(child[1], f, tabs)

def c_LINE(child, f, tabs):
    # 0: statement
    if child[0].label != 'SHELLBLOCK':
        for c in child.flatten('SHELLBLOCK'):
            toPython(c, f, tabs)

    toPython(child[0], f, tabs)

################################################################################
#
# Shell constructs
#
################################################################################

def c_SHELLBLOCK(child, f, tabs):
    # 0: statement

    toPython(child[0], f, tabs)

    # Replace the shell block with the variable as Python code
    child.label = 'PYTHON'
    child.children = [child.varname, ast(None, 'EMPTY')]

def c_PROCIN(child, f, tabs):
    # 0: command 1: instream 2: procout
    toPython(child[0], f, tabs)

    # TODO: Move this code into c_STREAM along with parsing of STREAM
    # Create the stream if it does not already exist
    f.write('try:\n')
    f.write(tabs + '    ' + phi + phi + ' = ')
    toPython(child[1], f, tabs)
    f.write('\n' + tabs + 'except (UnboundLocalError, NameError):\n')
    f.write(tabs + '    ')
    toPython(child[1], f, tabs)
    f.write(' = ' + phi + '.Stream()\n')

    f.write(tabs + child[0].varname + '.stdin = ')
    toPython(child[1], f, tabs)
    f.write('\n' + tabs)

    if child[2].label != 'EMPTY':
        toPython(child[2], f, tabs)

    child.parent.varname = child.varname

def c_PROC(child, f, tabs):
    # 0: command 1: procout

    toPython(child[0], f, tabs)

    if child[1].label != "EMPTY":
        toPython(child[1], f, tabs)

    child.parent.varname = child.varname

def c_COMMAND(child, f, tabs):
    # 0: command name 1: arglist

    child.parent.varname = child.varname
    
    f.write(child.varname + ' = ' + phi + ".Process('" + child[0] + "'")
    if child[1].label != "EMPTY":
        f.write(", ")
        toPython(child[1], f, tabs)
    f.write(")\n" + tabs)

    # # Repalce with python code
    # child.label = 'PYTHON'
    # child.children = [child.varname, ast(None, 'EMPTY')]

def c_ARGLIST(child, f, tabs):
    # 0: arg 1: arglist
    toPython(child[0], f, tabs)
    
    if child[1].label != "EMPTY":
        f.write(", ")
        toPython(child[1], f, tabs)

def c_ARG(child, f, tabs):
    # 0: argument
    if not isinstance(child[0], ast):
        f.write("'" + child[0] + "'")
    else:
        toPython(child[0], f, tabs)

def c_PIPE(child, f, tabs):
    # 0: stdout pipe target 1: stderr pipe target
    if child[0].label != 'EMPTY':
        toPython(child[0], f, tabs)
        f.write(child.parent.varname + '.stdout = ' + child[0].varname)

    if child[1].label != 'EMPTY':
        toPython(child[1], f, tabs)
        f.write(child.parent.varname + '.stderr = ' + child[1].varname)

def c_VAR(child, f, tabs):
    # 0: VARNAME
    f.write(child[0])

def c_STREAMOUT(child, f, tabs):
    # 0: stdout 1: stderr
    
    if child[0].label != 'EMPTY':

        # Create the stream if it does not already exist
        f.write('try:\n')
        f.write(tabs + '    ' + phi + phi + ' = ')
        toPython(child[0], f, tabs)
        f.write('\n' + tabs + 'except (UnboundLocalError, NameError):\n')
        f.write(tabs + '    ')
        toPython(child[0], f, tabs)
        f.write(' = ' + phi + '.Stream()\n')

        # Link the stream as stdout
        f.write(tabs + child.parent.varname + '.stdout = ')
        toPython(child[0], f, tabs)
        f.write('\n' + tabs)

    if child[1].label != 'EMPTY':

        # Create the stream if it does not already exist
        f.write('try:\n')
        f.write(tabs + '    ' + phi + phi + ' = ')
        toPython(child[1], f, tabs)
        f.write('\n' + tabs + 'except (UnboundLocalError, NameError):\n')
        f.write(tabs + '    ')
        toPython(child[1], f, tabs)
        f.write(' = ' + phi + 'Stream()\n')

        # Link the stream as stdout
        f.write(tabs + child.parent.varname + '.stderr = ')
        toPython(child[1], f, tabs)
        f.write('\n' + tabs)

functions = {
    "EMPTY"              : c_EMPTY,
    "PROGRAMFILE"        : c_PROGRAMFILE,
    "SHELLBLOCK"         : c_SHELLBLOCK,
    "PROCIN"             : c_PROCIN,
    "PROC"               : c_PROC,
    "COMMAND"            : c_COMMAND,
    "ARGLIST"            : c_ARGLIST,
    "ARG"                : c_ARG,
    "PIPE"               : c_PIPE,
    "BLOCK"              : c_BLOCK,
    "VAR"                : c_VAR,
    "SUITE_BLOCK"        : c_SUITE_BLOCK,
    "PYTHON"             : c_PYTHON,
    "STATEMENT_MULTI"    : c_STATEMENT_MULTI,
    "LINE"               : c_LINE,
    "STREAMOUT"          : c_STREAMOUT,
}
