#import numpy as np
from wrappers import *
from numpy import polyfit,array,shape,concatenate,ones

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
    segZ = array([])
    maxEnd = shape(data)[1]+1
    goodOne = ones(shape(data)[1])
    dSeg = array([])
    
    while end <= maxEnd:
        
        p,err,dis1,dis2,dis3 = polyfit(data[0,start:end],data[1,start:end],1,full = True)
        if shape(err)[0]<1: err = [0]
        
        if err[0]>=maxErr:
            tempSeg = data[0,start:end-1]*pOld[0]+pOld[1]
            segZ = concatenate((segZ,data[0,start:end-1]))
            dSeg = concatenate((dSeg,goodOne[start:end-1]*pOld[0]))
            start = end
            end += 1
            allP.append(pOld)
            segments = concatenate((segments,tempSeg))
            
        pOld = p    
        end += 1
        
    if start!=shape(data[0])[0]:    
        p,err,dis1,dis2,dis3 = polyfit(data[0,start:],data[1,start:],1,full = True)
        dSeg = concatenate((dSeg,goodOne[start:]*p[0]))
        segZ = concatenate((segZ,data[0,start:]))
        tempSeg = data[0,start:]*p[0]+p[1]
        allP.append(p)
        segments = concatenate((segments,tempSeg))
    
    allP = array(allP)
    print shape(allP)
    return (segZ,segments),allP,dSeg