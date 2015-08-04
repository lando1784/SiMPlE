import numpy as np
import mvobject
from peaks import *

class segment(mvobject.mvobject):
    def __init__(self,x,y):   
        #internal units
        #  sensitivity nm/V
        #  k pN/nm
        #  speed nm/s
        #  Z nm
        #  F pN
        #  directions are near | far | hold
        defaults = {'direction':'far','speed':1.0,'k':1.0,'type':'Vconst'}
        self.parseConfig(defaults,'Segment')
        if len(x)==0:
            return False
         
        if x[0]>x[-1]:
            self.direction='near'
            x.reverse()
            y.reverse()
            
        self.peaks = []
            
        self.show = True

        self.z = np.array(x)
        self.f = np.array(y) 


    def getRelevant(self):
        for i in range(len(self.z)):
            if self.z[i]>=0.0:
                start = i
                break
        return self.z[start:],self.f[start:]
        
            
    def FZtoFD(self):
        """
        Convert Force versus Displacement to Force versus Distance
        """
        self.z=self.z-self.f/self.k
        
        
    def getPeaks(self,peakFinder = None, peakModel = None, argsPF = [], kwArgsPF = {},id = ''):
        
        self.peaks = []
        self.peaks = Peaks(self.z,self.f,peakFinder, peakModel, argsPF, kwArgsPF,id)
        
        return len(self.peaks)
        
        
if __name__ == "__main__":
    print 'not for direct use'
