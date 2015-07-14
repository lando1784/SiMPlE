import numpy as np


def movingAvg(data,window):
    
    hWin = (window-window%2)/2
    hWinUp = (window+window%2)/2
    
    filtered = np.array(data)
    
    for i in np.arange(data.shape[0]-hWin-hWinUp+1)+hWin:
        filtered[i] = np.average(data[i-hWin:i+hWin])
        
    for i in xrange(hWin):
        filtered[i] = np.average(data[0:i+hWin])
        
    j = 0
    for i in np.arange(hWin)+(data.shape[0]-hWin):
        filtered[i] = np.average(data[i-hWin:i+hWin-j])
        j += 1
        
    return filtered


def movingComp(a,b,sym = '<',window = 10, oneOrdata = True):
    
    if type(a) is not np.ndarray:
        print '\'a\' must be an array'
        return None
    
    bArray = type(b) is np.ndarray
    hWin = (window-window%2)/2
    hWinUp = (window+window%2)/2
    
    filtered = np.array(a)
    
    for i in np.arange(a.shape[0]-hWin-hWinUp+1)+hWin:
        aClip = a[i-hWin:i+hWin]
        bClip = b[i-hWin:i+hWin] if bArray else b
        temp = eval('aClip'+sym+'bClip')
        filtered[i]=int(temp.all()) if oneOrdata else int(temp.all())*a[i] 
        
    for i in xrange(hWin):
        aClip = a[0:i+hWin]
        bClip = b[0:i+hWin] if bArray else b
        temp = eval('aClip'+sym+'bClip')
        filtered[i] = int(temp.all()) if oneOrdata else int(temp.all())*a[i]
        
    j=0
    for i in np.arange(hWin)+(a.shape[0]-hWin):
        aClip = a[i-hWin:i+hWin-j]
        bClip = b[i-hWin:i+hWin-j] if bArray else b
        temp = eval('aClip'+sym+'bClip')
        filtered[i] = int(temp.all()) if oneOrdata else int(temp.all())*a[i]
        j += 1
        
    return filtered


def WAThBRIF(binaryData):
    value1 = binaryData[0]
    value2 = binaryData[np.where(binaryData!=value1)[0]][0]
    ranges = []
    limits = []
    bMask = np.zeros(binaryData.shape[0])
    arrow = 122
    count = 1
    start = 0
    for i in xrange(binaryData.shape[0]-1):
        bMask[i] = int(binaryData[i]!=binaryData[i+1])*arrow
        if bMask[i]:
            arrow = 122 if binaryData[i] == value2 else 221
            ranges.append(count)
            count = 1
            end = i
            limit = [start,end]
            limits.append(limit)
            start = end+1
        else:
            count += 1
    limits.append([start,binaryData.shape[0]-1])
    ranges.append(count)
    resistance = zip(limits,ranges)
    print ranges[::2]
                
    return bMask,resistance


def contactIntruder(realData,binaryData,sym = '<'):
    
    resistance = WAThBRIF(binaryData)[1]
    
    apparentlyNC = resistance[1::2]
    
    
                
        
        
        
if __name__ == '__main__':
    
    p = np.array([1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,2,2,2,2,2])
    print WAThBRIF(p)
              
        
        
        
        