class OutStream:
    def __init__(self, stream):
        """ Creates the OutStream object using the underlying python stream
        given as an argument. The given stream must be readable. """
        self._stream = stream

    # This stream works as a generator of strings using the default bash IFS
    # which separates on space, tab, and newline.
    def __iter__(self):
        return self

    def __next__(self):
        """ This verison of __next__ separates on newline only. """
        line = self._stream.__next__()
        if isinstance(line, (bytes, bytearray)):
            return str(line, encoding='utf-8').rstrip('\n\r')
        return line.rstrip('\n\r')
    
    # def __next__(self):
    #     """ This version of __next__ separates on all whitespace. """
    #     data = ''
        
    #     # read one character
    #     char = self._stream.read(1)

    #     if not char:
    #         # empty char means EOF
    #         raise StopIteration
        
    #     # convert char to string if needed
    #     if isinstance(char, bytes):
    #         char = str(char, encoding='utf-8')
        
    #     while char:
    #         # consume whitespace as needed
    #         if data and char in [' ', '\t', '\n']:
    #             break

    #         if char not in [' ', '\t', '\n']:
    #             # add on the read in character unless it is whitespace
    #             data += char

    #         # read in another character
    #         char = self._stream.read(1)
    #         # convert char to string if needed
    #         if isinstance(char, bytes):
    #             char = str(char, encoding='utf-8')
        
    #     return data
