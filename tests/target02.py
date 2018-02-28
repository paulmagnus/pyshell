from pyshell.procedure import Procedure
from subprocess import PIPE, Popen
import os
import io
import stat
import sys

# (Procedure("ls") | Procedure("cat")).run()
proc = Procedure("ls")
proc._ostreamtype = PIPE
proc._begin_process()
out_stream = proc.get_ostream()
print(out_stream)
# os.dup2(1, out_stream.fileno())
print(sys.stdout.fileno())
os.write(1, b"hello\n")

# os.dup2(out_stream.fileno(), 5)
# os.fchmod(out_stream.fileno(), stat.S_IWUSR)
# print(os.read(out_stream.fileno(), 10).decode('utf-8'))
# # os.write(out_stream.fileno(), b"hi")
# print(os.read(out_stream.fileno(), 10).decode('utf-8'))
# print(out_stream.read().decode('utf-8'))

# clean up
os.closerange(3,10)

# def fd_test():
#     return os.open('target02.py', os.O_RDONLY)

# Popen(['cat'], stdin=fd_test())