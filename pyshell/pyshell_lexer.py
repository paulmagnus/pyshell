import sys

# These are the lexing states. Each state controls which
# tokens are used.
states = (
    ('shell', 'exclusive'),
    ('indent', 'exclusive'),
)

tokens = [
    # SHELL TOKENS
    "PIPE",                     # |
    "STREAM_OUT",               # >
    "STREAM_IN",                # <
    "LPAREN",                   # (
    "RPAREN",                   # )
    "COMMA",                    # ,
    "SHELL_DELIMITER",          # $

    # COMPLEX SHELL TOKENS
    "FILEOUT",                  # ->
    "FILEAPPEND",               # >>
    "ERRPIPE",                  # !|
    "BOTHPIPE",                 # &|
    "ERROUT",                   # !>
    "BOTHOUT",                  # &>

    # SHELL CONTRUCTS
    "VARNAME",                  # Python variable name
    "STRING",                   # Python string
    "WORD",                     # Bash word
    
    # PYTHON
    "PYTHON",
    "DOCSTRING",
    "NL",
    "INDENT",
    "DEDENT",
]

# SHELL TOKENS
t_shell_PIPE = r'\|'
t_shell_STREAM_OUT = r'>'
t_shell_STREAM_IN = r'<'
t_shell_LPAREN = r'\('
t_shell_RPAREN = r'\)'
t_shell_COMMA = r','

# COMPLEX SHELL TOKENS
t_shell_FILEOUT = r'\->'
t_shell_FILEAPPEND = r'>>'
t_shell_ERRPIPE = r'\!\|'
t_shell_BOTHPIPE = r'\&\|'
t_shell_ERROUT = r'\!>'
t_shell_BOTHOUT = r'\&>'

# SHELL CONSTRUCTS
t_shell_WORD = r'(([^\s\|><\(\),\-\!\&\$])|' + \
               r'(\-(?![>]))|' + \
               r'(\!(?![\|>]))|' + \
               r'(\&(?![\|>]))|' + \
               r'((?<=\\)(?s).))+' # escaped characters

t_ANY_NL = r'\n'

t_ANY_ignore_WS =  r'[ \t]'

t_ANY_STRING = r'((?<!\\)\'.*?(?<!\\)\')|((?<!\\)\".*?(?<!\\)\")'

t_PYTHON = r'[^\$\'\"\s]+'

def t_DOCSTRING(t):
    r'((?<!\\)"""(?s).*?(?<!\\)""")|((?<!\\)\'\'\'(?s).*?(?<!\\)\'\'\')'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_SHELL_DELIMITER(t):
    r'(?<!\\)\$'
    t.lexer.push_state('shell')
    return t

def t_shell_SHELL_DELIMITER(t):
    r'(?<!\\)\$'
    t.lexer.pop_state()
    return t

def t_shell_VARNAME(t):
    r'@[a-zA-Z_][a-zA-Z0-9_]*'
    t.value = t.value[1:]
    return t

def t_CONTLINE(t):
    r'\\[\s\t]*\n[\s\t]*'
    t.lexer.lineno += t.value.count('\n')
    return t

# skip blank lines at the beginning
def t_pass_start(t):
    r'^([ \t]|\n|\#.*)+'
    t.lexer.lineno += t.value.count('\n')
    if t.value[-1] == ' ' or t.value[-1] == '\t':
        last_nl = t.value.rfind('\n')
        t.value = len(t.value[last_nl + 1:])
        t.type = "INDENT"
        t.lexer.indentedline = t.lineno
        t.lexer.indentstack.append(t.value)
        return t

def t_INITIAL_NL(t):
    r'\n[ \t]*(?![\n\#])'
    t.lexer.lineno += t.value.count('\n')
    t.lexer.push_state('indent')
    t.lexer.skip(-1 * len(t.value))
    t.value = t.value[:1]
    return t
    
# ignore other blank lines
def t_pass(t):
    r'\n[ \t]*(?=[\n\#])'
    t.lexer.lineno += 1

def t_comment(t):
    r'\#[^n]*'
    pass

def t_indent_INDENT(t):
    r'\n[ \t]*(?![\n\#])'
    t.value = t.value[1:]

    # Statements are in line with each other; no indentation occuring
    if len(t.value) == t.lexer.indentstack[-1]:
        t.lexer.pop_state()

    # Dedent occurs when the indentation level is less than the previous
    # indent on the stack
    elif len(t.value) < t.lexer.indentstack[-1]:
        t.type = "DEDENT"
        t.lexer.skip(-1 * len(t.value) - 1)
        t.value = t.lexer.indentstack[-1]
        t.lexer.indentstack.pop()
        return t

    else:
        # Normal indent: return the indent token
        t.lexer.pop_state()
        prev_indent = t.lexer.indentstack[-1]
        t.value = len(t.value)
        t.lexer.indentedline = t.lineno
        t.lexer.indentstack.append(t.value)
        return t

# TODO: Something strange is happening with the error checking
def t_shell_error(t):
    print("Shell syntax error")

def t_error(t):
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

def t_indent_error(t):
    print("Lex indent error on Line " + str(t.lineno), file=sys.stderr)

# lexer = lex.lex()
