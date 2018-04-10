def convert_to_str(s):
    if isinstance(s, bytes):
        s = str(s, encoding='utf-8')
    return s

class Stream:
    def __init__(self):
        """ Creates the OutStream object using the underlying python stream
        given as an argument. The given stream must be readable. """
        self._running = False
        self._stdin = None
        self._stdout = None
        self._flushed = False

        # The underlying stream once this is run
        self._stream = None

    def set_in_stream(self, stream):
        self._stream = stream

        if self.stdout is not None:
            self.stdout.set_in_stream(stream)

    @property
    def stdin(self):
        return self._stdin

    def set_stdin(self, stdin):
        self._stdin = stdin

        stdin.set_flushed(self.flushed)
        return self

    @property
    def stdout(self):
        return self._stdout

    def set_stdout(self, s):
        self._stdout = s
        self._stdout.set_stdin(self)
        return self

    @property
    def flushed(self):
        return self._flushed

    def set_flushed(self, f):
        self._flushed = f

        if f:
            if self.stdin is not None:
                self.stdin.flush()
            else:
                self.run()

        return self

    def flush(self):
        self.set_flushed(True)
        return self

    def run(self):
        # force run this stream

        if self._running:
            return self

        self._running = True

        # Force the input to run if needed
        if self.stdin is not None:
            self.stdin.run()

        if self.stdout is not None:
            self.stdout.run()

        return self

    def remove(self, other):
        if self.stdin is other:
            self._stdin = None
        elif self.stdout is other:
            self._stdout = None
        else:
            print('Remove failed')

    def __del__(self):
        # print('Deleting', self)
        if self.stdin is not None:
            self.stdin.remove(self)
        self.flush()
        # print('Done deleting', self)

    # This stream works as a generator of strings using the default bash IFS
    # which separates on space, tab, and newline.
    def __iter__(self):
        self.run()
        return self

    # def __next__(self):
    #     """ This verison of __next__ separates on newline only. """
    #     line = self._stream.__next__()
    #     if isinstance(line, (bytes, bytearray)):
    #         return str(line, encoding='utf-8').rstrip('\n\r')
    #     return line.rstrip('\n\r')
    
    def __next__(self):
        """ This version of __next__ separates on all whitespace. """
        data = ''
        
        # read one character
        char = self._stream.read(1)

        if not char:
            # empty char means EOF
            raise StopIteration
        
        # convert char to string if needed
        char = convert_to_str(char)
        
        while char:
            # consume whitespace as needed
            if data and char in [' ', '\t', '\n']:
                break

            if char not in [' ', '\t', '\n']:
                # add on the read in character unless it is whitespace
                data += char

            # read in another character
            char = self._stream.read(1)
            # convert char to string if needed
            if isinstance(char, bytes):
                char = str(char, encoding='utf-8')
        
        return data

class FileStream(Stream):
    pass

class InFileStream(FileStream):
    def __init__(self, filename):
        Stream.__init__(self)
        
        self._filename = filename
        self._file = None

    def __iter__(self):
        self._file = open(self._filename, 'r')
        return self

    def __next__(self):
        data = ''
        
        char = convert_to_str(self._file.read(1))

        if not char:
            # Empty char means EOF
            raise StopIteration

        while char:
            # Consume whitespace as needed
            if data and char in [' ', '\t', '\n']:
                break

            if char not in [' ', '\t', '\n']:
                # Add on the read in character unless it is whitespace
                data += char

            # Read in another character
            char = convert_to_str(self._file.read(1))

        return data

class OutFileStream(FileStream):
    def __init__(self, filename):
        self._filename = filename
        self._file = None

