import sys
sys.path.append("/home/pmagnus/HonorsProject/pyshell/")
from process import Process
if (Process('ls').run()):
	print('hi')
