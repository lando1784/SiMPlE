#import numpy as np
from wrappers import *
from numpy import polyfit,array,shape,concatenate

def myRegression(sequence, seq_range):
    """Return (x0,y0,x1,y1) of a line fit to a segment of a sequence using linear regression"""
    p, error = leastsquareslinefit(sequence,seq_range)
    y0 = p[0]*seq_range[0] + p[1]
    y1 = p[0]*seq_range[1] + p[1]
    return (seq_range[0],y0,seq_range[1],y1),p,error


def mySlidingWindow(data,maxErr = 0.3):
    
    start = 0
    end = start+2
    
    allP = []
    segments = array([])
    maxEnd = shape(data)[1]+1
    
    while end <= maxEnd:
        
        p,err,dis1,dis2,dis3 = polyfit(data[0,start:end],data[1,start:end],1,full = True)
        print "Start: " + str(start)
        print "End: " + str(end)
        print err
        print p
        if err>=maxErr:
            tempSeg = data[0,start:end]*p[0]+p[1]
            start = end
            end += 1
            allP.append(p)
            segments = concatenate((segments,tempSeg))
            
            
        end += 1
        
    return segments,allP