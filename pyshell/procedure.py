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

        # Output types
        # These are used for setting the stdout and stderr values for Popen
        self._ostreamtype = None
        self._errstreamtype = None

        # The running procedure
        self._proc = None

        # These first two might not be necessary in the end
        self._procedure_name = procedure_name
        self._args = args

        # This should be used for actually building the Popen object
        self._proc_list = [self._procedure_name] + list(args)

    def run(self):
        """
        Temporary method for when there is not output handling involved.
        """
        if self._proc is None:
            self._proc = Popen(self._proc_list,
                               stdin=self._istream,
                               stdout=self._ostreamtype,
                               stderr=self._errstreamtype)
            
            # set up output streams for PIPE if needed
            if self._ostreamtype == PIPE:
                self._ostream = self._proc.stdout
            
            if self._errstreamtype == PIPE:
                self._errstream = self._proc.stderr
        else:
            raise ProcessRuntimeException

    def begin_process(self):
        """
        Begins the process running. If the process has already started,
        a ProcessRuntimeException is raised.
        """

        if self._proc is None:
            self._proc = Popen(self._proc_list,
                               stdin=self._istream,
                               stdout=self._ostreamtype,
                               stderr=self._errstreamtype)
            self._ostream = self._proc.stdout
            self._errstream = self._proc.stderr
        else:
            raise ProcessRuntimeException

    def set_input_stream(self, stream):
        """ Changes the input stream of the process. """
        self._istream = stream

    def pipe_output(self):
        self._ostreamtype = PIPE
        self._errstreamtype = PIPE

    def pipe(self, proc):
        """
        Pipes the output of this process into the input stream
        of the argument proc. Returns a reference to proc.
        """
        if not isinstance(proc, Procedure):
            raise TypeError("unsupported operand type(s) for |: '" +
                            type(self).__name__ + "' and '" +
                            type(proc).__name__) + "'"

        self.pipe_output()
        
        if self._proc is None:
            self.run()

        proc.set_input_stream(self._ostream)
        return proc

    def get_ostream(self):
        """ Returns the output stream of the process. """
        return self._ostream

    def get_errstream(self):
        """ Returns the error stream of the process. """
        return self._errstream

    # This needs a new name
    def write(self, ostream=sys.stdout.buffer, errstream=sys.stderr.buffer):
        """ Writes the output and error output to their respective buffers. """

        if self._proc is None:
            self.begin_process()

        # Note that this might not do them in the correct order currently.
        ostream.write(self._ostream.read())
        errstream.write(self._errstream.read())

    def __or__(self, proc):
        """ Implements the | operator for this object """
        if not isinstance(proc, Procedure):
            raise TypeError("unsupported operand type(s) for |: '" +
                            type(self).__name__ + "' and '" +
                            type(proc).__name__) + "'"
        
        return self.pipe(proc)

    # def __ror__(self, proc): # see 3.3.7 at
    # https://docs.python.org/3/reference/datamodel.html#special-method-names

    def __gt__(self, other):
        """ Implements the > operator for this object. """
        pass

    def __del__(self):
        # probably not the best but it ensures that this program is done before
        # ending the Python script
        # self._proc.communicate()

        # use for debugging
        print("Object being deleted")

        # clean up
        # self._proc.kill()

class ProcessRuntimeException(Exception):
    """
    This is an exception that is raised when there is a problem with the
    process while it is running.
    """
    pass
