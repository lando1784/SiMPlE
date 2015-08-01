import numpy as np
from fitLib import *

class peak(object):
    
    def __init__(self,z,f,model = None):
        
        self.z = z
        self.f = f
        self.model = model
        self.fit = None
        
    
    def getGrowth(self):
        
        return self.z[:self.apex[0]],self.f[:self.apex[0]]
    
    
    def getLength(self):
        
        return self.z[-1]-self.z[0]
    
    
    def getBaseLine(self):
        
        return np.mean(self.f[self.apex[0]+1:])
        
    
    def getHeight(self):
        
        return self.apex[1]-self.getBaseline()
    
    
    def getArea(self):
    
        step = np.mean(self.z[1:]-self.z[:-1])
        deltas = self.f-self.getBaseLine()
        deltas[np.where(deltas<0)[0]] = 0
        
        area = np.sum(deltas*step)
    
        return area
    
    
    def getApex(self):
        
        return [z[np.where(self.f==np.max(self.f))][0][0],np.max(self.f)]
    
    
    def fitGrowth(self,fitModel = None):
        
        if fitModel == None:
            if self.model == None:
                raise ValueError('You haven\'t specified a model for your peak')
            fitModel = self.model
        gZ,gF = self.getGrowth()
        
        self.fit = genericFit(gZ,gF,fitModel)
        
    
    def getInfo(self):
        
        info = ''
        info += 'Peak length [nm]: ' + str(self.getLength()) + '\n'
        info += 'Peak height [pN]: ' + str(self.getHeight()) + '\n'
        info += 'Peak area [zJ]: ' + str(self.getArea()) + '\n'
        info += 'Starting point [nm]: ' + str(self.z[0]) + '\n'
        info += 'Ending point [nm]: ' + str(self.z[-1]) + '\n'
        
        apex = self.getApex()
        
        info += 'Peak apex position [nm]' + str(apex[0]) + '\n'
        info += 'Peak apex force [pN]' + str(apex[1]) + '\n'
        

class Peaks(object):
    
    def __init__(self, z, f, peakFinder = None, peakModel = None, argsPF = [], kwArgsPF = {}):
        
        self.zTrack = z
        self.fTrack = f
        
        self.peaks = []
        
        self.basicStats = {'areaM':None,'areaV':None,'heightM':None,'heightV':None,'lengthM':None,'lengthV':None}
        
        self.searchTheTrack(z,f,peakFinder,peakModel,argsPF,kwArgsPF)
    
    
    def __getitem__(self,index):
        
        return self.peaks[index]
        
    
    def __iter__(self):
        
        return self.peaks.__iter__()
    
    
    def __delitem__(self,index):
        
        del self.peaks[index]
        
    
    def append(self,obj):
        
        if isinstance(obj, peak):
            self.peaks.append(obj)
        else:
            raise ValueError('Youtried to append a non\'peak\' object')
        
        
    def searchTheTrack(self,z,f,pfFun,modelFun,pfArgs,pfKwargs):
        
        fpeaks,zpeaks = pfFun(z,f,*pfArgs,**pfKwargs)
        
        for i in xrange(len(fpeaks)):
            
            self.peaks.append(peak(zpeaks[i],fpeaks[i],modelFun))
    
    
    def getBasicStats(self):
        
        if self.basicStats != None:
            return self.basicStats
        
        template = np.zeros(len(self.peaks))
        areas = template
        lengths = template
        heights = template
        
        for i in xrange(template):
            areas[i] = self.peaks[i].getArea()
            heights[i] = self.peaks[i].getHeight()
            lengths[i] = self.peaks[i].getLength()
            
        self.basicStats['areaM'] = np.mean(areas)
        self.basicStats['areaV'] = np.var(areas)
        self.basicStats['heightM'] = np.mean(heights)
        self.basicStats['heightV'] = np.var(heights)
        self.basicStats['lengthM'] = np.mean(lengths)
        self.basicStats['lengthV'] = np.var(lengths)
        
        return self.basicStats
    
    
    def getStatFileEntry(self):
        
        if self.basicStats == None:
            self.getBasicStats()
            
        entry = np.array([self.basicStats['areaM'],self.basicStats['areaV'],self.basicStats['heightM'],
                          self.basicStats['heightV'],self.basicStats['lengthM'],self.basicStats['lengthV']])
        
        return entry











        
        