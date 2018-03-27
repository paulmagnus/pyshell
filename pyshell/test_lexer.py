import sys
import ply.lex as lex

tokens = [
    "SHELL_DELIMITER",
    # "STRING",
    "CODE",
    "NL",
    # "CONTINUE_LINE",
]

t_SHELL_DELIMITER = r'\$'
# t_STRING = (r'((?<!\\)\'([^\n]|\\\n)*?(?<!\\)\')|' + # single quote
#             r'((?<!\\)\"([^\n]|\\\n)*?(?<!\\)\")|' + # double quote
#             r'(\'\'\'(?s).*?\'\'\')|' +              # single docstring
#             r'("""(?s).*?""")')                      # double docstring
t_CODE = (r'(([^\'\"\n\\\$]|(\\\')|(\\\")|(\\\\)|(\\\$))|' +
          r'((?<!\\)\'([^\n]|\\\n)*?(?<!\\)\')|' + # single quote
          r'((?<!\\)\"([^\n]|\\\n)*?(?<!\\)\")|' + # double quote
          r'(\'\'\'(?s).*?\'\'\')|' +              # single docstring
          r'("""(?s).*?"""))+')                    # double docstring
t_NL = r'\n'
# t_CONTINUE_LINE = r'\\' # This might need some tweaking

def t_error(t):
    print("pyshell : Syntax Error", file=sys.stderr)

lex.lex()