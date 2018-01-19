"""
Test of new Procedure class
"""

from pyshell.procedure import Procedure

# target program:
# ls

# Procedure("ls").run()

# print("----------------------------")

# target program:
# ls | grep 2.py
# Procedure("ls").pipe(Procedure("grep", "2.py")).run()

# print("----------------------------")

# testing out | usage
(Procedure("ls") | Procedure("grep", "2.py")).run()

# print("----------------------------")

# target program:
# ls | less
# this causes strange output
# (Procedure("ls") | Procedure("less")).run()

# less does not work the same way that these previous things work

# print("----------------------------")

# (Procedure("ls", "-al") | Procedure("cat")).run()

# print("----------------------------")

# Procedure("cat", "target02.py").run()

# Interactive cat fails
# Procedure("cat").run()
