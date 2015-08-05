from peaks import peak, Peaks
import numpy as np
import scipy as sp
from PyInstaller.lib.unittest2.test.test_break import self

class peaksAnalyzer(object):
    
    def __init__(self,dir = ''):
        
        self.analytes = {}
        
        if dir != '':
            self.populateMe(dir)
            
    
    def populateMe(self,dir):
        
        tempPeaks = Peaks()
        
        if not self.peaks.loadDir(dir):
            return None 
        lastID = 0
        analyte = {}
        
        for p in tempPeaks:
            self.analytes[lastInd].append()