"""
Procedure.py

This is the basic procedure class for running external programs through
the shell.
"""

# subprocess allows for basic interaction with external programs
from subprocess import Popen, PIPE
import sys

class Procedure:
    """
    This is the basic procedure class for running external programs
    through the shell. Each instance is one external procedure.
    """

    def __init__(self, procedure_name, *args):
        """ Creates a new Procedure using the given arguments. """

        # Input, output, and error streams
        self._istream = None
        self._ostream = None
        self._errstream = None

        # The running procedure
        self._proc = None

        # These first two might not be necessary in the end
        self._procedure_name = procedure_name
        self._args = args

        # This should be used for actually building the Popen object
        self._proc_list = [self._procedure_name] + list(args)

    def _begin_process(self):
        """
        Begins the process running. If the process has already started,
        a ProcessRuntimeException is raised.
        """

        if self._proc is None:
            self._proc = Popen(self._proc_list,
                               stdin=self._istream,
                               stdout=PIPE,
                               stderr=PIPE)
            self._ostream = self._proc.stdout
            self._errstream = self._proc.stderr
        else:
            raise ProcessRuntimeException

    def set_input_stream(self, stream):
        """ Changes the input stream of the process. """
        self._istream = stream

    def pipe(self, proc):
        """
        Pipes the output of this process into the input stream
        of the argument proc.
        """
        if self._proc is None:
            self._begin_process()

        proc.set_input_stream(self._ostream)

    def get_ostream(self):
        """ Returns the output stream of the process. """
        return self._ostream

    def get_errstream(self):
        """ Returns the error stream of the process. """
        return self._errstream

    def write(self, ostream=sys.stdout.buffer, errstream=sys.stderr.buffer):
        """ Writes the output and error output to their respective buffers. """

        # Note that this might not do them in the correct order currently.
        ostream.write(self._ostream.read())
        errstream.write(self._errstream.read())

class ProcessRuntimeException(Exception):
    """
    This is an exception that is raised when there is a problem with the
    process while it is running.
    """
    pass
