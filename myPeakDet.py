import numpy as np
import math

def findPeak_Triangle(acArray, derSeg, startInd = 0):
    
    oldVal = acArray[0]
    confAC = []
    peakAC = []
    peakInd = []
    
    for i in acArray:
        confAC.append(i)
        if len(confAC) == 3:
            if confAC[1]>confAC[0] and confAC[1]>confAC[2]:

                if np.abs(math.atan(confAC[1]))+np.abs(math.atan(confAC[2])) >= math.pi/2:
                    peakAC.append(confAC[1])
                    print confAC[1]
                confAC = [confAC[2]]
            else:
                confAC = [confAC[1],confAC[2]]
    
    for p in peakAC:
        peakInd.append(np.where(derSeg == p)[0][-1]+startInd)
    
    return peakAC, peakInd


def findPeak_Greater(acArray, derSeg, startInd = 0):
    
    oldVal = acArray[0]
    confAC = []
    peakAC = []
    peakInd = []
    
    for i in acArray:
        confAC.append(i)
        if len(confAC) == 3:
            if confAC[1]>confAC[0] and confAC[1]>confAC[2]:
                peakAC.append(confAC[1])
                confAC = [confAC[2]]
            else:
                confAC = [confAC[1],confAC[2]]
    
    for p in peakAC:
        peakInd.append(np.where(derSeg == p)[0][-1]+startInd)
    
    return peakAC, peakInd