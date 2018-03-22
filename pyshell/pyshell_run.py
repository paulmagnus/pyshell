import sys, re, os

tmp_path = "./"

def run(filename):

    find_path = re.compile('(?P<p>[\S]+)/(?P<n>[\S]+).pysh')
    found_path = find_path.search(filename)

    if found_path:
        name = tmp_path + "/" + found_path.group("n") + ".py"
    else:
        name = tmp_path + "/" + filename[:-5] + ".py"

    if not os.path.isfile(name):
        print("Error: Python executable does not exist", file=sys.stderr)
        remove_files()

    os.system('python3 ' + name)


