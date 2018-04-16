import sys, re, os
from pyshell import Process, Stream

tmp_path = "./"

def run(filename):

    find_path = re.compile('(?P<p>[\S]+)/(?P<n>[\S]+).pysh')
    found_path = find_path.search(filename)

    if found_path:
        name = tmp_path + "/." + found_path.group("n") + ".py"
    else:
        name = tmp_path + "/." + filename[:-5] + ".py"

    if not os.path.isfile(name):
        print("Error: Python executable does not exist", file=sys.stderr)
        remove_files()

    # if Process('pylint', name):
    Process('python3', name)
    # else:
    #     print('pylint errors')
