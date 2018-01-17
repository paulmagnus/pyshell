"""
This file is my first test of what Python code is needed in order to run scripts
and interact with their input and output.
"""

# CITE: https://docs.python.org/3/library/subprocess.html#module-subprocess
# for use of the subprocess module

# for most interactions with external programs
import subprocess
# for sys.stdout.buffer
import sys

# Target psudo program:
#
# ls | grep t

# Need to do something about the number of variables

PROC = subprocess.Popen(["ls"], stdout=subprocess.PIPE)

# mostly just trying out the with statement
with subprocess.Popen(["grep", "t"], stdin=PROC.stdout, stdout=subprocess.PIPE) as PROC2:
    # using the buffer here allows for the byte stream to be output correctly
    sys.stdout.buffer.write(PROC2.stdout.read())
