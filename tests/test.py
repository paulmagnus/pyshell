from pyshell import *

def delimiter():
    print("------------------------------------------------------------------")

# Code in bash
# { { ./bash01.sh 2>&3 | grep --color=auto test; } 3>&1 1>&4 | grep --color=auto error; } 4>&1

# Code in pyshell
# $./bash01.sh | (grep --color=auto test, grep --color=auto error)$

# Code using new Python library
proc0 = Process("./bash01.sh")
proc1 = Process("grep", "--color=auto", "test")
proc2 = Process("grep", "--color=auto", "error")
proc0.pipe(proc1, proc2)
proc1.run()
proc2.run()

delimiter()

# Code in bash
# while read line; do
#     echo "${line}"
# done < <(ls)

# Code in pyshell
# for line in $ls$:
#     print(line)

# Code using new Python library
for line in Process("ls"):
    print(line)

delimiter()

def foo(*args):
    print("Start--------------")
    for arg in args:
        print("Arg:", arg, file=sys.stderr)
    print("End----------------")
    return 0

proc = Process("foo", "here", "are", "the", "arguments")
proc1 = Process("grep", "--color=auto", "a")
proc.stderr = STDOUT
proc.pipe(proc1)
proc1.run()
print(proc.started)

# procs = []
# for _ in range(100):
#     procedure = Process("ls")
#     procedure.stdout = PIPE
#     procedure.run()
#     procs.append(procedure)
#     print(procedure.stdout)
