import sys
import re
import os
import getpass

from pyshell_files import get_tmp_path, extract_base_directory, \
    get_python_file, remove_files

def run(filename):

    name = get_python_file(filename)

    if not os.path.isfile(name):
        print("Error: Python executable does not exist", file=sys.stderr)
        remove_files(filename)

    script_dir = os.path.dirname(os.path.realpath(__file__))

    os.system(script_dir + '/bin/run_python ' + name + ' ' +
              extract_base_directory(filename))

    remove_files(filename)
