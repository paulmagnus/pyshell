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
# from pyshell.stream import OutStream

# __all__ = ['Process',
#            # Errors
#            'ProcessError',
#            'ProcessRunningError',
#            'ProcessStartedError',
#            'ProcessNotStartedError',
#            'ProcessTerminatedError',
#            'ProcessNotRunningError',
           
#            # Decorators
#            'process_not_started',
#            'process_started',
#            'process_running',
           
#            # Constants
#            'PIPE',
#            'DEVNULL',
#            'STDOUT']

# logging levels:
# CRITICAL  50
# ERROR     40
# WARNING   30
# INFO      20
# DEBUG     10
# NOTSET     0
logging.basicConfig(level=logging.DEBUG)

PIPE = sub.PIPE
DEVNULL = sub.DEVNULL
STDOUT = sub.STDOUT

# PROCESS STATES
INIT = 0
RUNNING = 1
TERMINATED = 2

class ProcessError(Exception):
    """ Base class for all process related exceptions. """
    pass

class ProcessStateError(ProcessError):
    """ The exception for when the current operation is not usable with
    the current state of the process. """
    pass

# Decorators
def process_states(*states):
    """ This decorator verifies that the process is in one of the states given
    by the list states at the moment that the method is called. """
    def decorator(function):
        def wrapper(*args, **kwargs):
            if args[0].state not in states:
                raise ProcessStateError
            return function(*args, **kwargs)
        return wrapper
    return decorator

def log(function):
    """ This decorator logs when the process starts and ends. """
    def wrapper(*args, **kwargs):
        logging.debug("Starting " + function.__name__)
        result = function(*args, **kwargs)
        logging.debug("Ending " + function.__name__)
        return result
    return wrapper

# def process_not_started(function):
#     """ This decorator checks to make sure that the method is called before the
#     process has been started. """
#     def wrapper(*args, **kwargs):
#         if args[0].started:
#             raise ProcessStartedError
#         return function(*args, **kwargs)
#     return wrapper

# def process_started(function):
#     """ This decorator checks to make sure that the method is called after
#     the process has been started. """
#     def wrapper(*args, **kwargs):
#         if not args[0].started:
#             raise ProcessNotStartedError
#         return function(*args, **kwargs)
#     return wrapper

# def process_running(function):
#     """ This decorator checks to make sure that the method is called while
#     the process is running. """
#     def wrapper(*args, **kwargs):
#         if not args[0].is_running():
#             raise ProcessNotRunningError
#         return function(*args, **kwargs)
#     return wrapper

# TODO: Note this is not thread safe at all
def redirect(function, *args,
             stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, **kwargs):
    # save sys.stdout and sys.stderr
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    # redirect stdout and stderr as needed
    sys.stdin = stdin
    sys.stdout = stdout
    sys.stderr = stderr

    result = function(*args, **kwargs)

    # return sys.stdout and sys.stderr
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    if not isinstance(result, int):
        # TODO: Write a better error message
        raise TypeError("Return code from '" +
                        str(function.__name__) +
                        "' must be an integer")

    return result

# TODO: Change name to Process
class Process2:
    def __init__(self, process_name: str, *args):
        self._proc_list = [process_name] + list(args)

        # I might not need this anymore
        self._proc = None

        ## Stream controls
        self._source = None
        self._out_target = None
        self._err_target = None

        self._return_code = None

    def run(self):
        # I'm done with this object
        pass

    def pipe(self, out_target=None, err_target=None):
        # send stdout and stderr of this process to specific locations
        self.stdout = out_target
        self.stderr = err_target
        return self

    @property
    def stdin(self):
        return self._source

    @stdin.setter
    def stdin(self, source):
        self._source = source

    @property
    def stdout(self):
        return self._out_target

    @stdout.setter
    def stdout(self, target):
        self._out_target = target

    @property
    def stderr(self):
        return self._err_target

    @stderr.setter
    def stderr(self, target):
        self._err_target = target

    def __iter__(self):
        # make this work like a generator
        pass

    @property
    def return_code(self):
        pass

    @property
    def state(self):
        pass

    # Control statements for the Popen objects being used
    def kill(self):
        pass

    def terminate(self):
        pass

    def send_signal(self, signal):
        pass

    

class Process:
    """ Instance of a single shell process. """

    def __init__(self, process_name: str, *args):
        """ Creates a new process using the given arguments. """

        # TODO: Type checking

        ## Script arguments
        self._proc_list = [process_name] + list(args)

        ## Popen process object
        # This is None until the process is started
        self._proc = None

        ## Stream controls
        # These control how Popen interacts with streams. The possible values
        # are as follows.
        # None - Use the default stream (for example using system stdout)
        # PIPE - Create a new stream object wrapper
        # DEVNULL - Discard the stream's data
        # STDOUT - Sends to the same place as stdout stream (only for stderr)
        # An existing file object or file descriptor (int) can be used.
        self._in_stream = None
        self._out_stream = None
        self._err_stream = None

        # get the frame where __init__was called
        self._frame = inspect.stack()[1][0]

        self._return_code = None

    @process_states(INIT)
    def run(self):
        """
        Currently, this is a wrapper for _begin_process
        """
        self._begin_process()

    @process_states(INIT)
    def pipe(self, out_proc=None, err_proc=None):
        """
        Pipes the output of this process into the input stream of the argument
        proc.

        If out_proc is given, then stdout is piped into out_proc. Similarly,
        if err_proc is given, then stderr is piped into err_proc.
        """

        if out_proc is not None and not isinstance(out_proc, Process):
            raise TypeError
        if err_proc is not None and not isinstance(err_proc, Process):
            raise TypeError

        # set up pipes
        if out_proc is not None:
            self.stdout = PIPE
        if err_proc is not None:
            self.stderr = PIPE

        # start the process running
        self._begin_process()

        if out_proc is not None:
            out_proc.stdin = self._out_stream
        if err_proc is not None:
            err_proc.stdin = self._err_stream
        return out_proc

    @property
    def stdin(self):
        """ The input stream of the process. """
        return self._in_stream

    @stdin.setter
    @process_states(INIT)
    def stdin(self, stream):
        """ Changes the input stream of the process. """

        # TODO: Type checking

        # TODO: Do we allow overwrites?

        self._in_stream = stream

    @property
    def stdout(self):
        """ The standard output stream of the process. """ 
        return self._out_stream

    @stdout.setter
    @process_states(INIT)
    def stdout(self, stream):
        """
        Changes the type of the stdout stream.

        The only legal values for stream are
            None
            PIPE
            DEVNULL
            an existing file or file descriptor
        """

        # TODO: Type checking

        # TODO: Do we allow overwrites?

        self._out_stream = stream

    @property
    def stderr(self):
        """ The standard error stream of the process. """
        return self._err_stream

    @stderr.setter
    @process_states(INIT)
    def stderr(self, stream):
        """
        Changes the type of the stderr stream.

        The only legal values for stream are
            None
            PIPE
            DEVNULL
            STDOUT
            an existing file or file descriptor
        """

        # TODO: Type checking

        # TODO: Do we allow overwrites?

        self._err_stream = stream

    # @process_not_started
    @process_states(INIT)
    def __iter__(self):
        """
        Begins the process, piping out the stdout as the iterator.
        """
        self.stdout = PIPE
        self._begin_process()
        
        # Wait can be dangerous but I think we're fine in this case.
        # self._proc.wait()

        # TODO: Build this stream class as a generator of strings
        # return OutStream(self.stdout)
        # return self.stdout
        return self

    def __next__(self):
        return str(self.stdout.__next__(), encoding='utf-8').rstrip()

    @property
    def return_code(self):
        """
        Returns the return code of the process.
        A value of None indicates that the process has not completed yet.
        """

        # Special case for if the process calls an interal Python function
        if self._return_code is not None:
            return self._return_code
        
        if self.started:
            return None
        self._return_code = self._proc.poll()
        return self._return_code

    @property
    def state(self):
        """ Returns the current state of the process. """
        if self._proc is None:
            return INIT
        if self._return_code is None:
            return RUNNING
        return TERMINATED

    def is_running(self):
        """
        Returns True if the process is currently running. False otherwise.

        A return value of False means that either the process has completed
        or it has not been started yet.
        """
        return self.started and self.return_code is None

    @property
    def started(self):
        """
        Returns True if the process has been started, otherwise returns False.
        """
        return self._proc is not None

    @property
    def terminated(self):
        """
        Returns True if the process has finished, otherwise returns False.
        """
        return self.started and self.return_code is not None

    @property
    @process_states(RUNNING, TERMINATED)
    def pid(self):
        """ Returns the process id. """
        return self._proc.pid

    @process_states(RUNNING)
    def kill(self):
        """
        Kills the process.
        On Posix OSs the function sends SIGKILL to the child.
        On Windows kill() is an alias for terminate().
        """
        self._proc.kill()

    @process_states(RUNNING)
    def terminate(self):
        """
        Stop the child.
        On Posix OSs the method sends SIGTERM to the child.
        On Windows the Win32 API function TerminateProcess() is called to
        stop the child.
        """
        self._proc.terminate()

    @process_states(RUNNING)
    def send_signal(self, signal):
        """ Sends the signal to the process. """
        self._proc.send_signal(signal)

    def _begin_function_process(self):
        """ Begins the process running only if the process is an internal python
        method or function. """

        # stdin
        in_read_stream = None
        
        if self._in_stream is None:
            # default to system stdin
            in_read_stream = sys.stdin

        else:
            in_read_stream = self._in_stream

        # out stream
        out_write_stream = None

        if self._out_stream is None:
            # default to system stdout
            self._out_stream = None
            out_write_stream = sys.stdout
            
        elif self._out_stream == PIPE:
            # create new stream object
            out_read_fd, out_write_fd = os.pipe()
            self._out_stream = io.BufferedReader(io.FileIO(out_read_fd,
                                                           mode='r'))
            out_write_stream = io.TextIOWrapper(io.FileIO(out_write_fd,
                                                          mode='w'))

        elif self._out_stream == DEVNULL:
            # send to operating system's devnull
            self._out_stream = None
            out_write_stream = open(os.devnull, 'w')
        else:
            out_write_stream = self._out_stream

        # error stream
        err_write_stream = None
        
        if self._err_stream is None:
            # default to system stderr
            self._err_stream = None
            err_write_stream = sys.stdout

        elif self._err_stream == PIPE:
            # create new stream pipe
            err_read_fd, err_write_fd = os.pipe()
            self._err_stream = io.BufferedReader(io.FileIO(err_read_fd,
                                                           mode='r'))
            err_write_stream = io.TextIOWrapper(io.FileIO(err_write_fd,
                                                          mode='w'))

        elif self._err_stream == DEVNULL:
            # send to operating system's devnull
            self._err_stream = None
            err_write_stream = open(os.devnull, 'w')

        elif self._err_stream == STDOUT:
            # send to the same place as this process's stdout
            self._err_stream = self._out_stream
            err_write_stream = out_write_stream
            
        self._return_code = redirect(self._proc,
                                     *self._proc_list,
                                     stdin=in_read_stream,
                                     stdout=out_write_stream,
                                     stderr=err_write_stream)

    @process_states(INIT)
    def _begin_process(self):
        """
        Begins the process running.
        If the process was already running, a ProcessError is raised.
        """

        # TODO: Deal with KeyboardInterrupt

        # Use python function instead if it is available
        function_name = self._proc_list[0]
        if function_name in self._frame.f_locals:
            self._proc = self._frame.f_locals[function_name]
            self._begin_function_process()
        elif function_name in self._frame.f_globals:
            self._proc = self._frame.f_globals[function_name]
            self._begin_function_process()
        else:
            self._proc = sub.Popen(self._proc_list,
                                   stdin=self._in_stream,
                                   stdout=self._out_stream,
                                   stderr=self._err_stream)

            # Update output streams
            self._out_stream = self._proc.stdout
            self._err_stream = self._proc.stderr

            # TODO: I don't think this works generally enough
            # If there are no changes to the output and error streams,
            # wait until the process has finished to continue.
            if self._out_stream in [None, DEVNULL] and \
               self._err_stream in [None, DEVNULL, STDOUT]:
                self._proc.wait()

    # Operators and special interface methods
    # TODO: Determine difference between __repr__ and __str__ for this class
    def __repr__(self):
        return "Process <" + " ".join(self._proc_list) + ">"

    def __str__(self):
        return self.__repr__()

    @process_states(INIT)
    def __or__(self, other):
        """
        Implements | operator for this object. This is mostly
        syntactic sugar.
        """
        if isinstance(other, tuple):
            return self.pipe(*other)
        return self.pipe(other)

    # TODO: Do we need to implement __ror__?
    # def __ror__(self, proc): # see 3.3.7 at
    # https://docs.python.org/3/reference/datamodel.html#special-method-names

    @process_states(INIT)
    def __gt__(self, other):
        """ Implements the > operator for this object. """
        # TOOD: Implement __gt__
        raise NotImplementedError

    @process_states(INIT)
    def __lt__(self, other):
        """ Implements the < operator for this object. """
        # TODO: Implement __lt__
        raise NotImplementedError


