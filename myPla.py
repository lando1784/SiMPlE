import numpy as np


def myRegression(sequence, seq_range):
    """Return (x0,y0,x1,y1) of a line fit to a segment of a sequence using linear regression"""
    p, error = leastsquareslinefit(sequence,seq_range)
    y0 = p[0]*seq_range[0] + p[1]
    y1 = p[0]*seq_range[1] + p[1]
    return (seq_range[0],y0,seq_range[1],y1),p,error


def mySlidingWindows(data,maxErr = 0.005):
    
    start = 0
    end = 1
    
    