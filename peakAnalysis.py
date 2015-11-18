from peaks import peak, Peaks
import numpy as np
import scipy as sp

class peaksAnalyzer(object):
    
    
    funcDict = {'>': '>(','<': '<(','>=': '>=(','<=': '<=(',
                'l' : '.longer(','h':'.higher()'}
    
    
    def __init__(self,dir = '',values = None):
        
        if dir != '':
            self.populateMe(dir,True)
        elif values != None and dir == '':
            self.populateMe(dir, values)
        else:
            self.analytes = {'id':[]}
            self.ans = None
            
    
    def openDir(self,dir):        
        tempPeaks = Peaks()
        
        if not tempPeaks.loadDir(dir):
            return False
        else:
            return tempPeaks
    
    def populateMe(self,dir = '',peaksPack=None,reset = True):
        
        if reset:
            self.analytes = {'id':[]}
            self.ans = None
        
        if dir != '':
            tempPeaks = self.openDir(dir)
            if not tempPeaks:
                return None
        elif peaksPack != None and dir == '':
            tempPeaks = peaksPack
            if len(tempPeaks)<1:
                return False
        else:
            return None
        
        lastAID = 0
        lastID = tempPeaks[0].id
        self.analytes['id'].append(lastID)
        self.analytes[lastAID] = []
        
        for p in tempPeaks:
            if p.id != lastID:
                lastAID += 1
                lastID = p.id
                self.analytes['id'].append(lastID)
                self.analytes[lastAID] = []
                
            self.analytes[lastAID].append(p)
        return True
        
    
    def listIDs(self):
        i=0
        for id in self.analytes['id']:
            print str(i) + ') ' + id
            i+=1
            
    
    def __getitem__(self,index):
        
        if type(index) == str:
            ind = self.analytes['id'].index(index)
            return self.analytes[ind]
        return self.analytes[index]
    
    
    def __iter__(self):
        i = -1
        for id in self.analytes['id']:
            i+=1
            yield self.analytes[i]
            
            
    def apexBrowser(self,sym = '>',comp = 0.0, returnPeaks = False):
        
        ans = peaksAnalyzer()
        ansPeaks = Peaks()
        
        i=0
        for id in self.analytes['id']:
            for p in self.analytes[i]:
                result = eval('p.apex' + sym + 'comp')
                if result:
                    ansPeaks.append(p)
            i+=1
        ans.populateMe('', ansPeaks)
        
        self.ans = ans
        
        if returnPeaks:
            return ans,ansPeaks
        return ans
    
    
    def peakBrowser(self,sym = '>', comp = 0.0, returnPeaks = False):
        ans = peaksAnalyzer()
        ansPeaks = Peaks()
        if sym not in self.funcDict.keys():
            raise ValueError('The function you selected is not included in the preloaded list')
        i=0
        for id in self.analytes['id']:
            for p in self.analytes[i]:
                result = eval('p' + self.funcDict[sym] + 'comp)')
                if result:
                    ansPeaks.append(p)
            i+=1
        ans.populateMe('', ansPeaks)
        
        if not ans:
            if returnPeaks:
                return None, None
            return None

        
        self.ans = ans
        
        if returnPeaks:
            return ans,ansPeaks
        return ans
    
    
