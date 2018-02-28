from subprocess import Popen, PIPE

my_stream = None
for i in range(10):
    print(my_stream)
    if my_stream is None:
        my_stream = Popen(['ls'], stdout=PIPE).stdout
    else:
        my_stream = Popen(['cat'], stdin=my_stream, stdout=PIPE).stdout
Popen(['cat'], stdin=my_stream)