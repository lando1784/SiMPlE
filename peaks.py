import numpy as np
from fitLib import *
import os
from os import makedirs
from os.path import split, join, splitext, exists, isfile

class peak(object):
    
    def __init__(self,z,f,baseLine = None,model = None,id=''):
        
        self.z = z
        self.f = f
        self.model = model
        self.fit = None
        self.id = id
        self.baseLine = baseLine
        
        self.apex = self.getApex()
    
    def getGrowth(self):
        
        return self.z[:self.apex[0]],self.f[:self.apex[0]]
    
    
    def getLength(self):
        
        return self.z[-1]-self.z[0]
    
    
    def getBaseLine(self):
        
        if self.baseLine is not None:
            return self.baseLine
        
        baseline = np.mean(self.f[self.apex[0]+1:])
        
        if str(baseline) == 'nan':
            baseline = np.min(self.f)
            
        self.baseLine = baseline
        
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
    
    
    def __add__(self,p2):
        
        if isinstance(p2,peak):
            return self.getArea() + p2.getArea()
        else:
            raise TypeError('A peak can only be added to another peak')
        
        
    def __radd__(self,p2):
        if p2 == 0:
            return self
        else:
            return self.__add__(p2)
        
        
    def __sub__(self,p2):
        
        if isinstance(p2,peak):
            return self.getArea() - p2.getArea()
        else:
            raise TypeError('A peak can only be subtracted to another peak')
        
        
    def __gt__(self,p2):
        
        if isinstance(p2,peak):
            return self.getArea() > p2.getArea()
        return self.getArea() > p2
    
    
    def __lt__(self,p2):
        
        if isinstance(p2,peak):
            return self.getArea() < p2.getArea()
        return self.getArea() < p2
    
    
    def __ge__(self,p2):
        
        if isinstance(p2,peak):
            return self.getArea() >= p2.getArea()
        return self.getArea() >= p2
    
    
    def __le__(self,p2):
        
        if isinstance(p2,peak):
            return self.getArea() <= p2.getArea()
        return self.getArea() <= p2
    
    
    def longer(self,p2):
        if isinstance(p2,peak):
            return self.getLength() > p2.getLength()
        return self.getLength() > p2
    
    
    def higher(self,p2):
        if isinstance(p2,peak):
            return self.getHeight() > p2.getHeight()
        return self.getHeight() > p2
    
    
    def fitGrowth(self,fitModel = None):
        
        if fitModel == None:
            if self.model == None:
                raise ValueError('You haven\'t specified a model for your peak')
            fitModel = self.model
        gZ,gF = self.getGrowth()
        
        self.fit = genericFit(gZ,gF,fitModel)
        
    
    def savePeak(self,filePath):
        if splitext(filePath)[1] != '.pkf':
            filePath = splitext(filePath)[0]+'.pkf'
        fileText = '#Peak ID:\t' + self.id + '\n'
        fileText += '#\n'
        fileText += '#\n'
        fileText += '#Displacement [nm]\tForce [pN]\n'
        fileText += '#\n'
        for i in xrange(len(self.z)):
            fileText += str(self.z[i])+'\t'+str(self.f[i])+'\n'
        outputFile = open(filePath,'w')
        outputFile.write(fileText)
        
    
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
    
    def __init__(self, z = None, f = None, peakFinder = None, peakModel = None, argsPF = [], kwArgsPF = {}, collectionID = ''):

        self.readMode = False
        self.peaks = []     

        if z is None:
            return None
        
        self.zTrack = z
        self.fTrack = f
        
        self.searchTheTrack(z,f,peakFinder,peakModel,argsPF,kwArgsPF,collectionID)
    
    
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
            raise ValueError('You tried to append a non\'peak\' object')
        
        
    def searchTheTrack(self,z,f,pfFun,modelFun,pfArgs,pfKwargs,id=''):
        
        returned = pfFun(z,f,*pfArgs,**pfKwargs)
        
        fpeaks = returned[0]
        zpeaks = returned[1]
        
        if len(returned)>2:
            baselines = returned[2]
        else:
            baselines = [None]*len(fpeaks)
        
        for i in xrange(len(fpeaks)):
            if zpeaks[i].shape[0]<=1:
                continue
            self.peaks.append(peak(zpeaks[i],fpeaks[i],baselines[i],modelFun,id))
    
    
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
    
    
    def saveCollection(self,dir,baseName='',overWrite = False):
        
        if not exists(dir):
            makedirs(dir)
        
        noBase = baseName == ''
        
        i = 0
        
        for p in self.peaks:
            fname = p.id if noBase else baseName + '_' + str(i)
            if exists(join(dir,fname)):
                fname += '_bis' if not overWrite else ''
            p.savePeak(join(dir,fname))
            i+=1
    
    
    def changeMode(self,mode = None):
        
        if mode == self.readMode:
            return None
        if mode is None:
            mode = not self.readMode
        
        self.readMode = mode
        
        self.peaks = []
    
    
    def loadPKF(self,filePath):

        if not self.readMode:
            return None
        
        pf = open(filePath)
        
        data = []
        
        first = pf.readline()
        id = (first.split('\t')[1]).split('\n')[0]

        for l in pf.readlines():
            if l.find('#') != -1:
                continue
	    if l[0] == '\n':
                continue
            dataChunk = np.array([float(d) for d in l.split('\t')])
            data.append(dataChunk)
        data = np.array(data)      

        return peak(data[:,0],data[:,1],id = id)
    
    
    def loadDir(self,dir):
        
        self.changeMode(True)     

        files = [f for f in os.listdir(dir) if isfile(join(dir,f)) and splitext(f)[1] == '.pkf']

        if files == []:
            return False
        files.sort()
        
        for f in files:
            self.peaks.append(self.loadPKF(join(dir,f)))
            
        return True
    
    
        






        
        
