#import numpy as np
from wrappers import *
from numpy import polyfit,array,shape,concatenate,ones


class PLA(object):
    
    def __init__(self,method,data,maxErr = 0.5):
        
        self.plaSegs,self.ACs,self.dSegs,self.startInds,self.endInds = method(data,maxErr)
        
    def getSeg(self,ind):
        
        el = {'values':self.plaSegs[ind],
              'AngCoeff':self.ACs[ind],
              'dSeg':self.dSegs[ind],
              'start':self.startInds[ind],
              'end':self.endInds[ind]
              }
        return el
    
    
    def getPlot(self):
        
        plot = array([])
        
        for s in self.plaSegs:
            
            plot = concatenate((plot,array(s)))
            
        return plot
    
    def getDplot(self):
        
        plot = array([])
        
        for d in self.dSegs:
            
            plot = concatenate((plot,array(d)))
            
        return plot
    


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
    return (segZ,segments),allP[:,0],dSeg


def mySlidingWindow_2(data,maxErr = 0.3):
    
    start = 0
    end = start+2
    
    allP = []
    segments = []
    startInd = []
    endInd = []
    maxEnd = shape(data)[1]+1
    goodOne = ones(shape(data)[1])
    dSeg = []
    
    while end <= maxEnd:
        
        p,err,dis1,dis2,dis3 = polyfit(data[0,start:end],data[1,start:end],1,full = True)
        if shape(err)[0]<1: err = [0]
        
        if err[0]>=maxErr:
            tempSeg = data[0,start:end-1]*pOld[0]+pOld[1]
            startInd.append(start)
            endInd.append(end-1)
            dSeg.append(goodOne[start:end-1]*pOld[0])
            start = end
            end += 1
            allP.append(pOld[0])
            segments.append(tempSeg)
            
        pOld = p    
        end += 1
        
    if start!=shape(data[0])[0]:    
        p,err,dis1,dis2,dis3 = polyfit(data[0,start:],data[1,start:],1,full = True)
        startInd.append(start)
        endInd.append(shape(data)[1]-1)
        dSeg.append(goodOne[start:]*p[0])
        tempSeg = data[0,start:]*p[0]+p[1]
        allP.append(p[0])
        segments.append(tempSeg)
    
    return segments,allP,dSeg,startInd,endInd