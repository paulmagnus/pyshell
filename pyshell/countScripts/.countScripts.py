import sys
sys.path.append("/home/pmagnus/pyshell/pyshell/")
import process as φ
numScripts = 0 
numLines = 0 
scriptLengths = [] 
φ0 = φ.Process('find', '/', '-type', 'f')
for name in φ0 : 
    φ1 = φ.Process('file', '-b', name)
    φ2 = φ.Process('grep', 'shell script')
    φ1.stdout = φ2
    if name != '-' and φ1 : 
        numScripts += 1 
        φ3 = φ.Process('sed', '/^\s*$/d', name)
        φ4 = φ.Process('wc', '-l')
        φ3.stdout = φ4
        linesInFile = int(iter( φ3 )[0]) 
        numLines += linesInFile 
        scriptLengths += [linesInFile] 
print( 'Total number of detected shell scripts:' , numScripts) 
print( 'Total number of lines in detected scripts:' , numLines) 
averageLinesPerFile = numLines / numScripts 
print( 'Average number of lines per file:' , averageLinesPerFile) 
scriptLengths = sorted(scriptLengths) 
minimum = scriptLengths[0] 
maximum = scriptLengths[-1] 
boxWidth = (maximum - minimum) / 10 
print( '\n----- Histogram -----\n' ) 
print( 'Min:' , minimum) 
print( 'Max:' , maximum) 
for i in range(10): 
    ne the bounds 
        lowerBound = minimum + boxWidth * i 
        upperBound = minimum + boxWidth * (i + 1) 
        count = 0 
        for length in scriptLengths: 
            if lowerBound <= length < upperBound: 
                count += 1 
        print( 'Box ' + str(i) + ':' ) 
        print( 'Bounds:' , lowerBound, upperBound) 
        print( 'Count:' , count) 
print( '\n----- End Histogram -----\n' ) 
firstQuartile = scriptLengths[int((maximum - minimum) / 4)] 
midpoint = scriptLengths[int((maximum - minimum) / 2)] 
thirdQuartile = scriptLengths[int((maximum - minimum) * 3 / 4)] 
print( '----- Box Plot -----' ) 
print( 'Min:' , minimum) 
print( 'First Quartile:' , firstQuartile) 
print( 'Median:' , midpoint) 
print( 'Third Quartile:' , thirdQuartile) 
print( 'Max:' , maximum) 
print( '----- End Box Plot -----' ) 
