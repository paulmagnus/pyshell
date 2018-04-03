import sys, re, os, pickle
from data_struct import ast

tmp_path = './'
line_num = 0
lines = {
    # python line : pyshell line
}

def translate(parsetree, filename):

    find_path = re.compile('(?P<p>[^/]+)/(?P<n>[^/]+).pysh')
    found_path = find_path.search(filename)

    global path
    if found_path:
        filename = found_path.group('n') + '.py'
        path = found_path.group("p") + "/"
    else:
        filename = filename[:-5] + '.py'
        path = ""

    if path != "":
        # replace ./ in path if it exists
        if re.match(r"^\./.+$", path):
            # first character is a .
            # replace with current working directory (cwd)
            path = os.getcwd() + path[1:]
        elif re.match(r"^[^/].+$", path):
            path = os.getcwd() + "/" + path

    # TRANSLATE
    try:
        with open(tmp_path + filename, 'w+') as python_file:
            toPython(parsetree, python_file)
        export_map(filename)
    except IOError:
        print("Can't translate " + tmp_path + filename + " due to IOError.",
              file = sys.stderr)
        remove_files()
        sys.exit(1)

    # return overloads

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

def c_EMPTY(child, f, tabs):
    pass

def c_PROGRAMFILE(child, f, tabs):
    # 0: shellblock

    f.write(tabs + 'import sys\n')
    advance(child)
    # f.write(tabs + 'sys.path.append("' + path + '")\n')
    # advance(child)
    
    # add pyshell to the search path
    script_path = re.match(r'(?P<path>.*/)[^/]+',
                           os.path.realpath(__file__)).group('path')
    f.write(tabs + 'sys.path.append("' + script_path + '")\n')
    advance(child)

    f.write(tabs + 'from process import Process\n')
    advance(child)

    toPython(child[0], f, tabs)

def c_BLOCK(child, f, tabs):
    # 0: statment_complex 1: nonempty_block
    toPython(child[0], f, tabs)
    toPython(child[1], f, tabs)

def c_STATEMENT_NO_RESULT(child, f, tabs):
    # 0: statement
    f.write(tabs)
    toPython(child[0], f, tabs)
    f.write('\n')

def c_SHELLBLOCK(child, f, tabs):
    # 0: statement

    toPython(child[0], f, tabs)

    f.write(".run()")
    advance(child)

def c_STATEMENT(child, f, tabs):
    toPython(child[0], f, tabs)

def c_PROCIN(child, f, tabs):
    pass

def c_PROC(child, f, tabs):
    # 0: command 1: procout

    toPython(child[0], f, tabs)

    if child[1].label != "EMPTY":
        toPython(child[1], f, tabs)

def c_COMMAND(child, f, tabs):
    # 0: command name 1: arglist
    
    f.write("Process('" + child[0] + "'")
    if child[1].label != "EMPTY":
        f.write(", ")
        toPython(child[1], f, tabs)
    f.write(")")

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

def c_PROCOUT(child, f, tabs):
    # 0: output
    toPython(child[0], f, tabs)

def c_PIPE(child, f, tabs):
    # 0: stdout pipe target 1: stderr pipe target
    f.write(".pipe(")
    if child[0].label != "EMPTY":
        f.write("out_proc=")
        toPython(child[0], f, tabs)
        if child[1].label != "EMPTY":
            f.write(", ")

    if child[1].label != "EMPTY":
        f.write("err_proc=")
        toPython(child[1], f, tabs)
    
    f.write(")")

def c_VAR(child, f, tabs):
    # 0: VARNAME
    f.write(child[0])

def c_CONDITIONAL(child, f, tabs):
    # 0: expression 1: suite 2: conditional_extension

    f.write(tabs + 'if (')
    toPython(child[0], f, tabs)
    f.write('):\n')
    advance(child)
    toPython(child[1], f, tabs+'\t')
    toPython(child[2], f, tabs)

def c_SUITE_BLOCK(child, f, tabs):
    # 0: block
    toPython(child[0], f, tabs)

def c_PYTHON(child, f, tabs):
    # 0: python code 1: further python code
    f.write(child[0])
    toPython(child[1], f, tabs)

functions = {
    "EMPTY"              : c_EMPTY,
    "PROGRAMFILE"        : c_PROGRAMFILE,
    "SHELLBLOCK"         : c_SHELLBLOCK,
    "STATEMENT"          : c_STATEMENT,
    "PROCIN"             : c_PROCIN,
    "PROC"               : c_PROC,
    "COMMAND"            : c_COMMAND,
    "ARGLIST"            : c_ARGLIST,
    "ARG"                : c_ARG,
    "PROCOUT"            : c_PROCOUT,
    "PIPE"               : c_PIPE,
    "BLOCK"              : c_BLOCK,
    "STATEMENT_NO_RESULT": c_STATEMENT_NO_RESULT,
    "VAR"                : c_VAR,
    "CONDITIONAL"        : c_CONDITIONAL,
    "SUITE_BLOCK"        : c_SUITE_BLOCK,
    "PYTHON"             : c_PYTHON,
}
