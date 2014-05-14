# -*- coding: utf-8 -*-
import numpy as np
import mvobject
from savitzky_golay import *
from smooth import *
import pla

def getmq(seg):
    dy = seg[3]-seg[1]
    dx = seg[2]-seg[0]
    m = dy/dx
    q = seg[3]-m*seg[2]
    return m,q

class segment(mvobject.mvobject):
    def __init__(self,x,y):   
        defaults = {'direction':'far','speed':1.0,'k':1.0,'type':'Vconst'}
        #internal units
        #  sensitivity nm/V
        #  k pN/nm
        #  speed nm/s
        #  Z nm
        #  F pN
        #  directions are near | far | hold
        
        self.parseConfig(defaults,'Segment')
        if len(x)==0:
            return False
         
        if x[0]>x[-1]:
            self.direction='near'
            x.reverse()
            y.reverse()
            
        self.show = True

        self.z = np.array(x)
        self.f = np.array(y) 
        self.PLA=None
    
    def look(self):
        import pylab
        pylab.figure()
        
        pylab.plot(self.z,self.f,label='Data')
        
        fragments = self.getPLA()
        if(len(fragments)>=2):
            pylab.plot((fragments[0][0],fragments[0][2]),(fragments[0][1],fragments[0][3]),'g--',label='Lin')
            pylab.plot((fragments[-1][0],fragments[-1][2]),(fragments[-1][1],fragments[-1][3]),'r--',label='Flat')
        else:
            print "No PLA available"
                    
        pylab.legend(loc=4)
        pylab.xlabel('Displacement [nm]')
        pylab.ylabel('Force [pN]')
        pylab.show()
        
    def getPLA(self,error=10000, Force=False):
        """
        NB: PLA is calculated over nm/nm data !!
        
        """
        if self.PLA != None and Force == False:
            return self.PLA
        PLA = pla.topdownsegment(self.f/self.k, pla.fit.interpolate, pla.fit.sumsquared_error, error)
        
        PLA = np.array(PLA)
        if len(PLA)>=2:
            PLA=[PLA[0],PLA[-1]]
        
        PLA[0][0] = self.z[PLA[0][0]]
        PLA[0][1] = self.k * PLA[0][1]
        PLA[0][2] = self.z[PLA[0][2]]
        PLA[0][3] = self.k * PLA[0][3]
        PLA[1][0] = self.z[PLA[1][0]]
        PLA[1][1] = self.k * PLA[1][1]
        PLA[1][2] = self.z[PLA[1][2]]
        PLA[1][3] = self.k * PLA[1][3]
                 
        self.PLA = PLA 
        return self.PLA
        
    def setCurve(self,error=10000.0):        
        fragments = self.getPLA(error)
                
        if(len(fragments)==2):
            m,q = getmq(fragments[1])

            self.f = self.f - (m*self.z+q)
            
            self.PLA[0][1] = self.PLA[0][1] - (m*self.PLA[0][0]+q)
            self.PLA[0][3] = self.PLA[0][3] - (m*self.PLA[0][2]+q)
            self.PLA[1][1] = self.PLA[1][1] - (m*self.PLA[1][0]+q)
            self.PLA[1][3] = self.PLA[1][3] - (m*self.PLA[1][2]+q)
            
            m,q = getmq(self.PLA[0])
            
            self.z = self.z+q/m
            
            self.PLA[0][0] = self.PLA[0][0] +q/m
            self.PLA[0][2] = self.PLA[0][2] +q/m
            self.PLA[1][0] = self.PLA[1][0] +q/m
            self.PLA[1][2] = self.PLA[1][2] +q/m
            
            mnm = m/self.k
            
            self.f=self.f/mnm
            
            self.PLA[0][1] = self.PLA[0][1]/mnm
            self.PLA[0][3] = self.PLA[0][3]/mnm
            self.PLA[1][1] = self.PLA[1][1]/mnm
            self.PLA[1][3] = self.PLA[1][3]/mnm
            
            return True 
        else:
            return False

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
        