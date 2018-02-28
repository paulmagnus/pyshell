"""
Procedure.py

This is the basic procedure class for running external programs through
the shell.
"""

# subprocess allows for basic interaction with external programs
from subprocess import Popen, PIPE
from io import IOBase
import sys
import logging

# logging levels:
# CRITICAL  50
# ERROR     40
# WARNING   30
# INFO      20
# DEBUG     10
# NOTSET     0
logging.basicConfig(level=logging.DEBUG)

SHELL_EXECUTABLE = None
# SHELL_EXECUTABLE = "/bin/bash"
SHELL = SHELL_EXECUTABLE is not None

logging.info("SHELL = " + str(SHELL))
logging.info("SHELL_EXECUTABLE = " + str(SHELL_EXECUTABLE))

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

        self._infile = None

        # Output types
        # These are used for setting the stdout and stderr values for Popen
        self._ostreamtype = None
        self._errstreamtype = None

        # The running procedure
        self._proc = None

        # These first two might not be necessary in the end
        self._procedure_name = procedure_name
        self._args = [str(arg) for arg in args]

        # This should be used for actually building the Popen object
        self._proc_list = [self._procedure_name] + list(self._args)
        
    def __repr__(self):
        """
        This method is used for determining the arguments of the Procedure,
        not the output since the output can be arbitrarily large.
        """
        return "Procedure <" + " ".join(self._proc_list) + ">"

    def run(self):
        """
        Runs a final Procedure. This should not be used internally as it waits
        for the process to complete before continuing with the python code.

        If the process is already running or has run in the past, a
        ProcessRuntimeException is raised.
        """
        if self._ostreamtype == PIPE:
            logging.warning("run was called but _ostreamtype = PIPE")
        if self._errstreamtype == PIPE:
            logging.warning("run was called but _errstreamtype = PIPE")

        try:
            self._begin_process()
        
            # WARNING: If PIPE was set this can cause strange errors according
            #          to the subprocess documentation.
            self._proc.wait()
        except KeyboardInterrupt:
            # No traceback on keyboard interrupt since this is just normal for
            # the system
            print()   # newline after ^C

    def get_pipe_streams(self, ostream, errstream):
        if ostream:
            self._ostreamtype = PIPE
        if errstream:
            self._errstreamtype = PIPE

        self._begin_process()

        return (self._ostream, self._errstream)

    def _begin_process(self):
        """
        Begins the process running. If the process has already started,
        a ProcessRuntimeException is raised.
        """
        
        if self._proc is None:
            if self._infile is not None:
                self._istream = open(self._infile, 'r')
            logging.debug("istream = " + str(self._istream))
            if self._istream is not None:
                logging.debug("open? " + str(not self._istream.closed))

            self._proc = Popen(self._proc_list,
                               stdin=self._istream,
                               stdout=self._ostreamtype,
                               stderr=self._errstreamtype,
                               shell=SHELL,
                               executable=SHELL_EXECUTABLE)

            # set up PIPE if needed
            if self._ostreamtype is not None:
                self._ostream = self._proc.stdout
                logging.debug("ostream = " + str(self._ostream.fileno()))
            if self._errstreamtype is not None:
                self._errstream = self._proc.stderr
                logging.debug("errstream = " + str(self._errstream.fileno()))
        else:
            # cannot begin the same process twice
            raise ProcessRuntimeException

    def set_input_stream(self, stream):
        """ Changes the input stream of the process. """

        logging.debug("stream = " + str(stream))

        if isinstance(stream, IOBase):
            self._istream = stream
        elif isinstance(stream, str):
            self._infile = stream
        else:
            self._istream = stream
        return self

    def pipe(self, proc, err_proc=None):
        """
        Pipes the output of this process into the input stream
        of the argument proc. Returns a reference to proc.

        If the err_proc argument is given, the stderr is piped
        into err_proc.
        """
        if not isinstance(proc, Procedure):
            raise TypeError("unsupported operand type for pipe: '" +
                            type(proc).__name__ + "'")

        if (err_proc is not None) and (not isinstance(err_proc, Procedure)):
            raise TypeError("unsupported optional operand type for pipe: '" +
                            type(err_proc).__name__ + "'")

        if self._proc is not None:
            # cannot begin same process twice
            raise ProcessRuntimeException

        # set up pipes
        self._ostreamtype = PIPE
        if err_proc is not None:
            self._errstreamtype = PIPE

        self._begin_process()

        # pass streams to processes
        proc.set_input_stream(self._ostream)
        if err_proc is not None:
            err_proc.set_input_stream(self._errstream)
        
        return proc

    def get_ostream(self):
        """ Returns the output stream of the process. """
        return self._ostream

    def get_errstream(self):
        """ Returns the error stream of the process. """
        return self._errstream

    # This needs a new name
    # def write(self, ostream=sys.stdout.buffer, errstream=sys.stderr.buffer):
    #     """ Writes the output and error output to their respective buffers. """

    #     if self._proc is None:
    #         self.begin_process()

    #     # Note that this might not do them in the correct order currently.
    #     ostream.write(self._ostream.read())
    #     errstream.write(self._errstream.read())

    def __or__(self, proc):
        """ Implements the | operator for this object """
        if not isinstance(proc, Procedure):
            raise TypeError("unsupported operand type(s) for |: '" +
                            type(self).__name__ + "' and '" +
                            type(proc).__name__ + "'")
        
        return self.pipe(proc)

    # def __ror__(self, proc): # see 3.3.7 at
    # https://docs.python.org/3/reference/datamodel.html#special-method-names

    def __gt__(self, other):
        """ Implements the > operator for this object. """
        raise NotImplementedError

    def __lt__(self, other):
        """ Implements the < operator for this object. """
        # TODO: check types
        return self.set_input_stream(other)

    def __del__(self):
        """
        This method is automatically called when the object is about to be
        removed. My hope is to somehow use this to stop the system from ending
        Python before the Process has completed - at least in most cases.
        """
        logging.debug("----- Start deletion of " + str(self) + " -----")
        
        # probably not the best but it ensures that this program is done before
        # ending the Python script
        # self._proc.communicate()

        # also not a good method but I'll leave it here in case part of this
        # is needed
        # while self._proc.poll() is None:
        #     pass

        # similarly bad method - website does not suggest when using PIPE
        # self._proc.wait()

        # use for debugging

        # clean up
        # self._proc.kill()

        logging.debug("----- " + str(self) + " deleted -----")

class ProcessRuntimeException(Exception):
    """
    This is an exception that is raised when there is a problem with the
    process while it is running.
    """
    pass
