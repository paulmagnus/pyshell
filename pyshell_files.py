import getpass
import re
import os
import sys

def get_tmp_path():
    return '/tmp/' + getpass.getuser()

def extract_base_name(pyshell_filename):
    find_path = re.compile('(?P<p>[\S]+)/(?P<n>[\S]+)')
    found_path = find_path.search(pyshell_filename)

    if found_path:
        name = found_path.group('n')
    else:
        name = pyshell_filename

    if name[-5:] == '.pysh':
        name = name[:-5]

    return name

def extract_base_directory(pyshell_filename):
    find_path = re.compile('(?P<p>[\S]+)/(?P<n>[\S]+)')
    found_path = find_path.search(pyshell_filename)

    if found_path:
        path = found_path.group('p')
    else:
        path = os.getcwd()

    # update path based on the current working directory
    if re.match(r'^\./.+$', path):
        # first character is a .
        # replace with the current working directory
        path = os.getcwd() + path[1:]
        
    elif re.match(r'^[^/].+$', path):
        path = os.getcwd() + '/' + path

    return path

def get_python_file(pyshell_filename):
    return get_tmp_path() + '/' + extract_base_name(pyshell_filename) + '.py'

def get_linemap_name(pyshell_filename):
    return get_tmp_path() + '/' + extract_base_name(pyshell_filename) + \
        '_linemap'

def remove_files(pyshell_filename):
    return
    try:
        os.remove(get_python_file(pyshell_filename))
        os.remove(get_linemap_name(pyshell_filename))
    except:
        print('Error: temporary files were not deleted correctly',
              file=sys.stderr)
    finally:
        sys.exit(0)
