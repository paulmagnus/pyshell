"""
This file is my first test of what Python code is needed in order to run scripts
and interact with their input and output.
"""

# CITE: https://docs.python.org/3/library/subprocess.html#module-subprocess
# for use of the subprocess module

import subprocess

# Target psudo program:
#
# ls

subprocess.Popen(["ls"])
