"""
process.py

This is the basic process class for running external programs through the shell.
"""

import subprocess as sub
import logging
import sys
import io
import os
import inspect
import traceback

# logging levels:
# CRITICAL  50
# ERROR     40
# WARNING   30
# INFO      20
# DEBUG     10
# NOTSET     0
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

PIPE = sub.PIPE
DEVNULL = sub.DEVNULL
STDOUT = sub.STDOUT

# PROCESS STATES
INIT = 0
RUNNING = 1
TERMINATED = 2

tabs = ''

def log(function):
    """ This decorator logs when the process starts and ends. """
    def wrapper(*args, **kwargs):
        global tabs
        logging.debug(tabs + "Starting " + function.__name__)
        tabs += '  '
        result = function(*args, **kwargs)
        tabs = tabs[:-2] # Remove the two spaces
        logging.debug(tabs + "Ending " + function.__name__)
        return result
    return wrapper

class Process:

    STDIN = 0
    STDOUT = 1
    STDERR = 2

    PIPE = sub.PIPE
    DEVNULL = sub.DEVNULL
    STDOUT = sub.STDOUT
    
    ### TREE SETUP
    def __init__(self, process_name, *args):
        self._proc_list = [process_name] + list(args)

        self._proc = None

        self._stdin = None
        self._stdout = None
        self._stderr = None

        self._return_code = None

        self._flushed = True
        self._running = False
        self._stream = None

    @property
    def stdin(self):
        return self._stdin

    @stdin.setter
    def stdin(self, stdin):
        self._stdin = stdin
        
        if (isinstance(stdin, (Process, Stream)) and
            self._stdin.stdout is not self):
            self._stdin.stdout = self

    @property
    def stdout(self):
        return self._stdout

    @stdout.setter
    def stdout(self, stdout):
        self._stdout = stdout

        if (isinstance(self._stdout, (Process, Stream)) and
            self._stdout.stdin is not self):

            self._stdout.stdin = self
            self._stdout.stdin_type = Stream.STDOUT

    @property
    def stderr(self):
        return self._stderr

    @stderr.setter
    def stderr(self, stderr):
        self._stderr = stderr

        if (isinstance(self._stderr, (Process, Stream)) and
            self._stderr.stdin is not self):

            self._stderr.stdin = self
            self._stderr.stdin_type = Stream.STDERR

    @property
    def stdin_type(self):
        return None

    @stdin_type.setter
    def stdin_type(self, _):
        pass

    @property
    def flushed(self):
        return self._flushed

    @flushed.setter
    def flushed(self, _):
        self._flushed = ((self._stdout is None or
                          not isinstance(self._stdout, (Process, Stream)) or
                          self._stdout.flushed) and
                         (self._stderr is None or
                          not isinstance(self._stderr, (Process, Stream)) or
                          self._stderr.flushed))

        if self.flushed:
            if (self._stdin is not None and
                isinstance(self._stdout, (Process, Stream))):
                self._stdin.flush()
            else:
                self.run()

    def flush(self):
        self.flushed = True
    
    def pipe(self, stdout=None, stderr=None):

        # only overwrite if the parameter is not None
        if stdout is not None:
            self.stdout = stdout
        if stderr is not None:
            self.stderr = stderr

    def run(self):
        # force the process to run

        if self._running:
            return

        # Force the input to run if needed
        if (self._stdin is not None and
            isinstance(self._stdin, (Process, Stream))):
            self._stdin.run()

        # Run this process
        self._begin_process()

        # Run all output
        if (self._stdout is not None and
            isinstance(self._stdout, (Process, Stream))):
            self._stdout.run()
        if (self._stderr is not None and
            isinstance(self._stderr, (Process, Stream))):
            self._stderr.run()

    @property
    def return_code(self):
        self.run()

        return self._proc.poll()

    def __bool__(self):
        return self.return_code == 0

    def __int__(self):
        return self.return_code

    def __iter__(self):
        if self.stdout is not None:
            return self._stdout.__iter__()
        else:
            self.stdout = Stream()
            return self._stdout.__iter__()

    def remove(self, other):
        if self._stdin is other:
            self._stdin = None
        elif self._stdout is other:
            self._stdout = None
        elif self._stderr is other:
            self._stderr = None
        else:
            print('Remove failed')

    def __del__(self):
        self.flush()

    def __str__(self):
        return ' '.join(self._proc_list)

    def _begin_process(self):
        self._running = True

        if isinstance(self._stdin, str):
            stdin = open(self._stdin, 'r')
        else:
            stdin = self._stdin

        if self._stdout is None:
            stdout = None
        elif isinstance(self._stdout, str):
            stdout = open(self._stdout, 'w')
        else:
            stdout = Process.PIPE

        if self._stderr is None:
            stderr = None
        elif self._stderr is self._stdout:
            stderr = Process.STDOUT
        elif isinstance(self._stderr, str):
            stderr = open(self._stderr, 'w')
        else:
            stderr = Process.PIPE

        # Bug: If this is called during __del__ when the program ends (not when
        # a function call ends) then sub.Popen will try to import a package but
        # the python system does not allow any new imports at this point.
        
        # Begin the process running
        try:
            self._proc = sub.Popen(self._proc_list,
                                   stdin=stdin,
                                   stdout=stdout,
                                   stderr=stderr)
        except TypeError as e:
            if sys.meta_path is None:
                # Incorrectly identified import error
                # CITE: https://bugs.python.org/issue26637
                # Also, this error does not fix itself by importing the same
                # package earlier in the code, unfortunately.
                raise ImportError('sys.meta_path is None, Python is likely '
                                  'shutting down. Consider moving all pyshell '
                                  'statements to inside functions.')
            else:
                raise

        if self.stdout is not None and isinstance(self._stdout,
                                                  (Stream, Process)):
            self._stdout.stdin = self._proc.stdout

        if self.stderr is not None and isinstance(self._stderr,
                                                  (Stream, Process)):
            self._stderr.stdin = self._proc.stderr
            
        if self.stdout is None and self.stderr is None:
            self._proc.wait()

def convert_to_str(s):
    if isinstance(s, bytes):
        s = str(s, encoding='utf-8')
    return s
            
class Stream:

    # Link input to stream
    STDOUT = 1
    STDERR = 2
    
    def __init__(self):
        self._reset()

    def _reset(self):
        self._stdin = None
        self._stdout = None
        self._stdin_type = None
        self._flushed = False
        self._running = False
        
    @property
    def stdin(self):
        return self._stdin

    @stdin.setter
    def stdin(self, stdin):
        self._stdin = stdin
        
        if self._stdout is not None:

            # Link stdin to stdout
            if self._stdin_type == Stream.STDERR:
                self._stdin.stderr = self._stdout
            else:
                self._stdin.stdout = self._stdout

            # Linking is done, reinitialize
            self._reset()
            
        else:
            self._stdin = stdin

    @property
    def stdout(self):
        return self._stdout

    @stdout.setter
    def stdout(self, stdout):
        self._stdout = stdout
        
        if self._stdin is not None:

            # Link stdin to stdout
            if self._stdin_type == Stream.STDERR:
                self._stdin.stderr = self._stdout
            else:
                self._stdin.stdout = self._stdout

            # Linking is done, reinitialize
            self._reset()
            
        else:
            self._stdout = stdout

    @property
    def stdin_type(self):
        return self._stdin_type

    @stdin_type.setter
    def stdin_type(self, stdin_type):
        self._stdin_type = stdin_type

    @property
    def flushed(self):
        return self._flushed

    @flushed.setter
    def flushed(self, flushed):
        self._flushed = flushed

        if self.flushed:
            if self.stdin is not None:
                self._stdin.flush()
            else:
                self.run()

    def flush(self):
        self.flushed = True

    def __iter__(self):
        self.run()
        return self

    def __next__(self):

        data = ''

        char = self._stdin.read(1)

        if not char:
            # empty char means EOF
            raise StopIteration

        while char:
            char = convert_to_str(char)

            # consume whitespace as needed
            if char in [' ', '\t', '\n']:
                break
            
            data += char
            char = self._stdin.read(1)

        return data

    def run(self):
        if self._running:
            return

        self._running = True
        
        if self.stdin is not None and isinstance(self.stdin, (Process, Stream)):
            self._stdin.run()

        if self.stdout is not None:
            self._stdout.run()

    def __del__(self):
        self.flush()
