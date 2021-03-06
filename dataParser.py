import csv, sys
import numpy as np
from myScripts import process_text
import sys, os, codecs
reload(sys)
sys.setdefaultencoding('utf-8')

def parseCSV(filename, entriesToProcess):
    
    x = []
    y = []
    
    with open(filename, 'rU') as inputs:
        reader = csv.DictReader(inputs)
        i = 0
        for row in reader :
            try:
                y.append(row['Prediction'])
                x.append(process_text(row["Interview"]))
            except:
                print ("Error parsing ", i,"th entry")
                # control shouldn't be in this portion of Code
            i +=  1
            if (i >= entriesToProcess and entriesToProcess >= 0):
                break

    print ("Parsing done!")
    y = np.array(y)
    return x,y


    

def parseTestCSV(filename, entriesToProcess):
    
    x = []
    with open(filename, 'rU') as inputs:
        reader = csv.DictReader(inputs)
        i = 0
        for row in reader :
            try:
                x.append(process_text(row["Interview"]))
            except:
                print ("Error parsing ", i,"th entry")
                # control shouldn't be in this portion of Code
            i +=  1
            if (i >= entriesToProcess and entriesToProcess >= 0):
                break

    print ("Parsing done!")
    return x



if __name__ == "__main__" : 
    
    filename = sys.argv[1]
    entriesToProcess = int(sys.argv[2])
    
    x, y = parseCSV(filename, entriesToProcess)
    print len(x), len(y)    
    print "Bye"