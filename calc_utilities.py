import numpy as np
from scipy.signal import savgol_filter as sgf
from types import FunctionType
from matplotlib.colors import NP_CLIP_OUT

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
    
    if type(sym) is not str and str(type(sym)) is not '<type \'builtin_function_or_method\'>':
        return None
    
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
        temp = eval('aClip'+sym+'bClip') if type(sym) is str else sym(aClip,bClip)
        filtered[i]=int(temp.all()) if oneOrdata else int(temp.all())*a[i] 
        
    for i in xrange(hWin):
        aClip = a[0:i+hWin]
        bClip = b[0:i+hWin] if bArray else b
        temp = eval('aClip'+sym+'bClip') if type(sym) is str else sym(aClip,bClip)
        filtered[i] = int(temp.all()) if oneOrdata else int(temp.all())*a[i]
        
    j=0
    for i in np.arange(hWin)+(a.shape[0]-hWin):
        aClip = a[i-hWin:i+hWin-j]
        bClip = b[i-hWin:i+hWin-j] if bArray else b
        temp = eval('aClip'+sym+'bClip') if type(sym) is str else sym(aClip,bClip)
        filtered[i] = int(temp.all()) if oneOrdata else int(temp.all())*a[i]
        j += 1
        
    return filtered


def almost(a,b,thrPc = 10):
    if type(a)==type(b)==np.ndarray and a.shape == b.shape:
        #thr = min(np.std(a), np.std(b), thrPc*np.mean(b)/100) if thrPc != None else min(np.std(a), np.std(b))
        thr = thrPc*np.mean(b)/100
        result = (b-thr<=a<=b+thr).all()
    elif type(a) is np.ndarray and isinstance(b,(int,long,float,complex)):
        #thr = min(np.std(a), thrPc*b/100) if thrPc != None else np.std(a)
        thr = thrPc*b/100
        result = (b-thr<=a<=b+thr).all()
    elif isinstance(a,(int,float,long,complex)) and isinstance(b,(int,long,float,complex)):
        thr = thrPc*b/100
        result = b-thr<=a<=b+thr
    else:
        raise TypeError('You used a wrong set of types. The onyl available combinations are:\n- \'a\' scalar and \'b\' scalar\n- \'a\' array and \'b\' scalar\n- \'a\' array and \'b\' array\n')
    
    return result


def binaryDataOrganizer(binaryData,val1 = None, val2 = None):
    value1 = binaryData[0] if val1 == None else val1
    value2 = binaryData[np.where(binaryData!=value1)[0]][0] if val2 == None else val2
    ranges = []
    limits = []
    bMask = np.zeros(binaryData.shape[0])
    count = 1
    start = 0
    for i in xrange(binaryData.shape[0]-1):
        bMask[i] = int(binaryData[i]!=binaryData[i+1])
        if bMask[i]:
            #arrow = 122 if binaryData[i] == value2 else 221
            ranges.append(count)
            count = 1
            end = i
            limit = [start,end]
            limits.append(limit)
            start = end+1
        else:
            count += 1
    val1ISvalue1 = value1 == binaryData[0]
    limits.append([start,binaryData.shape[0]-1])
    ranges.append(count)
    v1A = {'r': ranges[int(not val1ISvalue1)::2],'l':limits[int(not val1ISvalue1)::2]}
    v2A = {'r': ranges[int(val1ISvalue1)::2],'l':limits[int(val1ISvalue1)::2]}
    
    archive = {value1: v1A,value2: v2A}
                
    return archive


def fitCnNC(seg,sym = '>',sgfWinPc = 10,sgfDeg = 3,compWinPc = 10,winged = True,wingPc = 10,thPc = 15,realCntPt = True):
    
    force = seg.f
    displ = seg.z
    k = seg.k
    sgfWin = force.shape[0]/100*sgfWinPc
    sgfWin += int(sgfWin%2==0)
    compWin = force.shape[0]/100*compWinPc
    compWin += int(compWin%2==0)
    sForce = sgf(force,sgfWin,sgfDeg)
    gForce = np.gradient(sForce)
    ggForce = np.gradient(gForce)
    gForceBi = movingComp(gForce,ggForce,sym,compWin)
    forceArchive = binaryDataOrganizer(gForceBi, 1.0, 0.0)
    
    #contGoodL = forceArchive[1.0]['l'][np.where(np.array(forceArchive[1.0]['r'])==max(forceArchive[1.0]['r']))[0][0]]
    contGoodL = forceArchive[1.0]['l'][0]
    contGoodRcutWing = (forceArchive[1.0]['r'][0]/100*wingPc)/2 if winged else 0
    #freeGoodL = forceArchive[0.0]['l'][np.where(np.array(forceArchive[0.0]['r'])==max(forceArchive[0.0]['r']))[0][0]]
    freeGoodL = forceArchive[0.0]['l'][-1]
    freeGoodRcutWing = (forceArchive[0.0]['r'][0]/100*wingPc)/2 if winged else 0

    contFit = np.polyfit(displ[(contGoodL[0]+contGoodRcutWing):(contGoodL[1]+1-contGoodRcutWing)], force[(contGoodL[0]+contGoodRcutWing):(contGoodL[1]+1-contGoodRcutWing)], 1)
    #freeFit = [0.0,np.average(force[(freeGoodL[0]+freeGoodRcutWing):(freeGoodL[1]+1-freeGoodRcutWing)])]
    freeFit = np.polyfit(displ[(freeGoodL[0]+freeGoodRcutWing):(freeGoodL[1]+1-freeGoodRcutWing)], force[(freeGoodL[0]+freeGoodRcutWing):(freeGoodL[1]+1-freeGoodRcutWing)], 1)
    
    interPt = (freeFit[1]-contFit[1])/(contFit[0]-freeFit[0])
    
    contEnd = np.where(displ<=interPt)[0][-1]+1
    freeStart = contEnd
    
    contZ = displ[:contEnd]
    freeZ = displ[freeStart:]
    contF = contZ*contFit[0]+contFit[1]
    freeF = freeZ*freeFit[0]+freeFit[1]
    
    realZ = displ[np.where(force>=freeF[0])[0][0]]
    realF = force[np.where(force>=freeF[0])[0][0]]
    
    ctPoint = [realZ,realF] if realCntPt else [displ[contGoodL[1]],sForce[contGoodL[1]]]
    
    allFit = [contF,freeF]
    
    valid = almost(contFit[0],k,thPc) and almost(freeFit[0]+k,k,thPc)
    
    return allFit, ctPoint, valid
    
        
        
if __name__ == '__main__':
    
    p = np.array([1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,2,2,2,2,2])
    z = np.arange(300)
    f = np.concatenate((np.arange(100)-100,np.zeros(200)))
    pRes = binaryDataOrganizer(p)
    keys = pRes.keys()
    keys.sort()
    for k in keys:
        print k
        print pRes[k]
    
    fitCnNC(z,f)
    