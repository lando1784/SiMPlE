import numpy as np
from fitLib import *

class peak(object):
    
    def __init__(self,z,f,model = None):
        
        self.z = z
        self.f = f
        self.model = model
        self.fit = None
        
        self.apex = self.getApex()
    
    def getGrowth(self):
        
        return self.z[:self.apex[0]],self.f[:self.apex[0]]
    
    
    def getLength(self):
        
        return self.z[-1]-self.z[0]
    
    
    def getBaseLine(self):
        
        baseline = np.mean(self.f[self.apex[0]+1:])
        
        if str(baseline) == 'nan':
            baseline = np.min(self.f)
        
        return baseline
        
    
    def getHeight(self):
        
        return self.apex[1]-self.getBaseLine()
    
    
    def getArea(self):
    
        step = np.mean(self.z[1:]-self.z[:-1])
        deltas = self.f-self.getBaseLine()
        deltas[np.where(deltas<0)[0]] = 0
        
        area = np.sum(deltas*step)
    
        return area
    
    
    def getApex(self):
        
        return [self.z[np.where(self.f==np.max(self.f))[0][0]],np.max(self.f)]
    
    
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
        info += 'Peak apex position [nm]' + str(self.apex[0]) + '\n'
        info += 'Peak apex force [pN]' + str(self.apex[1]) + '\n'
    
        return info
    
    
    def getStatsFileEntry(self,eStr = False, label = ''):
        
        entry = [self.z[0],self.z[-1],self.apex[0],self.apex[1],self.getBaseLine(),self.getArea()]
        
        if eStr:
            eTemp = ''
            for e in entry:
                eTemp += str(e)+'\t'
            entry = eTemp+'\n'
            if label != '':
                entry = label + '\t' + entry
        
        return entry
        

class Peaks(object):
    
    def __init__(self, z, f, peakFinder = None, peakModel = None, argsPF = [], kwArgsPF = {}):
        
        self.zTrack = z
        self.fTrack = f
        
        self.peaks = []
        
        self.searchTheTrack(z,f,peakFinder,peakModel,argsPF,kwArgsPF)
    
    
    def __getitem__(self,index):
        
        return self.peaks[index]
        
    
    def __iter__(self):
        
        return self.peaks.__iter__()
    
    
    def __delitem__(self,index):
        
        del self.peaks[index]
        
        
    def __len__(self):
        
        return len(self.peaks)
        
    
    def append(self,obj):
        
        if isinstance(obj, peak):
            self.peaks.append(obj)
        else:
            raise ValueError('Youtried to append a non\'peak\' object')
        
        
    def searchTheTrack(self,z,f,pfFun,modelFun,pfArgs,pfKwargs):
        
        fpeaks,zpeaks = pfFun(z,f,*pfArgs,**pfKwargs)
        
        for i in xrange(len(fpeaks)):
            if zpeaks[i].shape[0]<=1:
                continue
            self.peaks.append(peak(zpeaks[i],fpeaks[i],modelFun))
    
    
    def getBasicStats(self):
        
        basicStats = {'areaM':None,'areaV':None,'heightM':None,'heightV':None,'lengthM':None,'lengthV':None}
        
        areas = np.zeros(len(self.peaks))
        lengths = np.zeros(len(self.peaks))
        heights = np.zeros(len(self.peaks))
        
        for i in xrange(areas.shape[0]):
            areas[i] = self.peaks[i].getArea()
            heights[i] = self.peaks[i].getHeight()
            lengths[i] = self.peaks[i].getLength()
            
        basicStats['areaM'] = np.mean(areas)
        basicStats['areaV'] = np.var(areas)
        basicStats['heightM'] = np.mean(heights)
        basicStats['heightV'] = np.var(heights)
        basicStats['lengthM'] = np.mean(lengths)
        basicStats['lengthV'] = np.var(lengths)
        
        return basicStats
    
    
    def getStatsFileEntry(self,eStr = False, label = ''):
        
        basicStats = self.getBasicStats()
            
        entry = [basicStats['areaM'],basicStats['areaV'],basicStats['heightM'],
                 basicStats['heightV'],basicStats['lengthM'],basicStats['lengthV']]
        
        if eStr:
            eTemp = ''
            for e in entry:
                eTemp += str(e)+'\t'
            entry = eTemp+'\n'
            if label != '':
                entry = label + '\t' + entry
        
        return entry
    
    
    def getSinglePeakStatsEntries(self,eStr = False, label = ''):
        
        entries = [] if not eStr else ''
        
        for p in self.peaks:
            
            if not eStr:
                entries.append(p.getStatsFileEntry())
            else:
                entries += p.getStatsFileEntry(True,label)
        
        return entries







        
        