# import io, os

# read, write = os.pipe()
# read1, write1 = os.pipe()

# write_stream = io.BufferedWriter(io.FileIO(write, mode='w'))
# write_stream1 = io.BufferedWriter(io.FileIO(write1, mode='w'))
# read_stream = io.BufferedReader(io.FileIO(read, mode='r'))
# read_stream1 = io.BufferedReader(io.FileIO(read, mode='r'))

# write_stream.write(b"Hello\n")
# write_stream1.write(b"How are you?\n")
# write_stream.flush()
# write_stream1.flush()
# write_stream.write(b"I'm doing well.")
# write_stream1.write(b"Same")
# os.dup2(write, write1)
# write_stream.close()
# write_stream1.close()
# print(read_stream.read())

# class Stream:
#     def __init__(self):
#         pass

# from pyshell import *
# import sys
# import logging

# def add_file(*argv):
#     if argv[2] == '0':
#         print(str(sys.stdin.read(), 'utf-8'))
#     # f = open(argv[1], 'r')
#     # sys.stdout.write(f.read())
#     with open(argv[1], 'r') as f:
#         print(f.read())
#     return 0

# start = True
# for f in Process('ls', '--ignore=*~*'):
#     if not os.path.isdir(str(f,'utf-8').rstrip()):
#         print(f)
#         proc = Process('add_file',
#                        str(f, 'utf-8').rstrip(),
#                        str(int(start)))
#         if not start:
#             proc.stdin = stream
#         proc.stdout = PIPE
#         proc.run()
#         print('hi')
#         stream = proc.stdout
#         start = False

# print(str(stream.read(), 'utf-8'))

# proc = Process('ls')
# proc1 = Process('add_file', '__init__.py')
# proc.pipe(proc1)
# proc1.run()

# from pyshell.stream import OutStream

# stream = OutStream(open('test.py', 'r'))
# for word in stream:
#     print(word)

# class Tree:
#     def __init__(self, num, left, right):
#         print("Creating", num)
#         self._num = num
#         self._left = left
#         self._right = right

#     def __del__(self):
#         print("Deleting", self._num)


# def foo():
#     t = Tree(1, Tree(2, Tree(3, None, None), None), Tree(4, None, Tree(5, None, None)))
#     for i in range(100):
#         print(i)

# if __name__ == "__main__":
#     foo()

# from pyshell import *
# def f():
#     # $ls > @s$
#     # $grep --color=auto .py < @s > @s$
#     # $grep --color=auto pyshell < @s$

#     # p = Process('ls')
#     # # No input
#     # s = Stream()
#     # p.pipe(s)
    
#     # p = Process('grep', '--color=auto', '.py')
#     # s.set_stdout(p)
#     # s = Stream()
#     # p.pipe(s)

#     # p = Process('grep', '--color=auto', '.py')
#     # s.set_stdout(p)
#     # # No new stream output
#     # # No output control

#     s = Stream()
#     Process('ls').pipe(s)
#     for test in ['.py', 'pyshell', 'lexer']:
#         p = Process('grep', test)
#         s.set_stdout(p)
#         s = Stream()
#         p.pipe(s)

#     s.set_stdout(Process('cat'))

#     # $ls | grep hi$
# f()

from pyshell import *
import inspect

# def f():
#     # Process('ls').pipe(Process('grep', '--color=auto', '\.py'))
#     p2 = Process('grep', '--color=auto', '\.py')
#     try:
#         p2.stdin = s
#     except (UnboundLocalError, NameError):
#         s = Stream()
#         p2.stdin = s

#     p = Process('ls')
#     try:
#         p.stdout = s
#     except (UnboundLocalError, NameError):
#         s = Stream()
#         p.stdout = s


# f()
p = Process('ls', '-al')
p
