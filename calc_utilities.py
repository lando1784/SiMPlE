import numpy as np
from scipy.signal import savgol_filter as sgf
from types import FunctionType
from matplotlib.colors import NP_CLIP_OUT
import operator
from fitLib import *


def movingThing(data,window,thing,others = None):
    
    hWin = (window-window%2)/2
    hWinUp = (window+window%2)/2
    
    filtered = np.array(data)
    
    for i in np.arange(data.shape[0]-hWin-hWinUp+1)+hWin:
        filtered[i] = thing(data[i-hWin:i+hWin]) if others == None else thing(data[i-hWin:i+hWin],*others)
        
    for i in xrange(hWin):
        filtered[i] = thing(data[0:i+hWin]) if others == None else thing(data[0:i+hWin],*others)
        
    j = 0
    for i in np.arange(hWin)+(data.shape[0]-hWin):
        filtered[i] = thing(data[i-hWin:i+hWin-j]) if others == None else thing(data[i-hWin:i+hWin-j],*others)
        j += 1
        
    return filtered


def splitLinFit(x, y, controlVal, controlFunc, iterLim = 10, controlParams=None):
    
    tempX = np.array(x)
    tempY = np.array(y)
    fit = np.polyfit(tempX, tempY, 1)
    
    for i in xrange(iterLim):
        condition = controlFunc(fit[0],controlVal) if controlParams == None else controlFunc(fit[0],controlVal,*controlParams)
        if condition:
            return tempX,tempY,fit
        center = tempX.shape[0]/2
        tempXh1 = tempX[:center]
        tempYh1 = tempY[:center]
        tempXh2 = tempX[center:]
        tempYh2 = tempY[center:]
        fitH1 = np.polyfit(tempXh1, tempYh1, 1)
        fitH2 = np.polyfit(tempXh2, tempYh2, 1)
        if abs(fitH1[0]-controlVal)>abs(fit[0]-controlVal) and abs(fitH2[0]-controlVal)>abs(fit[0]-controlVal):
            return tempX,tempY,fit
        tempX = tempXh1 if abs(fitH1[0]-controlVal)<abs(fitH2[0]-controlVal) else tempXh2
        tempY = tempYh1 if abs(fitH1[0]-controlVal)<abs(fitH2[0]-controlVal) else tempYh2
        fit = fitH1 if abs(fitH1[0]-controlVal)<abs(fitH2[0]-controlVal) else fitH2
    
    return tempX,tempY,fit
        
        

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


def movingVar(data,window):
    
    hWin = (window-window%2)/2
    hWinUp = (window+window%2)/2
    
    filtered = np.array(data)
    
    for i in np.arange(data.shape[0]-hWin-hWinUp+1)+hWin:
        filtered[i] = np.var(data[i-hWin:i+hWin])
        
    for i in xrange(hWin):
        filtered[i] = np.var(data[0:i+hWin])
        
    j = 0
    for i in np.arange(hWin)+(data.shape[0]-hWin):
        filtered[i] = np.var(data[i-hWin:i+hWin-j])
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


def almost(a,b,thrPc = 10, rangeMax = 1.0, rangeMin=0.0):
    if type(a)==type(b)==np.ndarray and a.shape == b.shape:
        #thr = min(np.std(a), np.std(b), thrPc*np.mean(b)/100) if thrPc != None else min(np.std(a), np.std(b))
        thr = thrPc*np.mean(b)/100
        result = (b-thr<=a<=b+thr).all()
    elif type(a) is np.ndarray and isinstance(b,(int,long,float,complex)):
        #thr = min(np.std(a), thrPc*b/100) if thrPc != None else np.std(a)
        thr = thrPc*b/100
        result = b-thr<=a.all()<=b+thr
    elif isinstance(a,(int,float,long,complex)) and isinstance(b,(int,long,float,complex)):
        thr = thrPc*b/100 if b != 0.0 else thrPc*(rangeMax-rangeMin)/100.0
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


def fitCnNC(seg,sym = '>',sgfWinPc = 10,sgfDeg = 3,compWinPc = 10,thPc = 15,realCntPt = False):
    
    force = seg.f
    displ = seg.z
    k = seg.k
    compWin = force.shape[0]/100*compWinPc
    compWin += int(compWin%2==0)
    sForce = smartSgf(force,sgfWinPc,sgfDeg)
    gForce = smartSgf(force,sgfWinPc,sgfDeg,1)
    ggForce = smartSgf(force,sgfWinPc,sgfDeg,2)
    gForceBi = movingComp(gForce,ggForce,sym,compWin)
    forceArchive = binaryDataOrganizer(gForceBi, 1.0, 0.0)
    
    contGoodL = forceArchive[1.0]['l'][0]
    freeDispl = np.array([])
    freeForce = np.array([])
    for l in forceArchive[0.0]['l']:
        if l[0] >= contGoodL[1]:
            freeDispl = np.concatenate((freeDispl,displ[l[0]:l[1]]))
            freeForce = np.concatenate((freeForce,force[l[0]:l[1]]))
    #freeGoodL = forceArchive[0.0]['l'][np.where(forceArchive[0.0]['r']==np.max(forceArchive[0.0]['r']))[0][0]]

    #_,_,contFit = splitLinFit(displ[contGoodL[0]:contGoodL[1]/2+contGoodL[0]],force[contGoodL[0]:contGoodL[1]/2+contGoodL[0]], k, almost, 1, [5,1.0,0.0])
    contFit = np.polyfit(displ[contGoodL[0]:contGoodL[1]],force[contGoodL[0]:contGoodL[1]],1)
    #_,_,freeFit = splitLinFit(displ[freeGoodL[0]:freeGoodL[1]],force[freeGoodL[0]:freeGoodL[1]], 0.0, almost, 10, [10,1.0,-1.0])
    freeFit = np.polyfit(freeDispl,freeForce,1)
    
    if freeFit[0]!=0.0:
        center = freeDispl.shape[0]/2
        freeDp1 = freeDispl[:center]
        freeDp2 = freeDispl[center:]
        freeFp1 = freeForce[:center]
        freeFp2 = freeForce[center:]
        tempFit1 = np.polyfit(freeDp1,freeFp1,1)
        tempFit2 = np.polyfit(freeDp2,freeFp2,1)
        freeFit = tempFit1
        if abs(tempFit2[0])<abs(tempFit1[0]):
            freeFit = tempFit2
    
    interPt = (freeFit[1]-contFit[1])/(contFit[0]-freeFit[0])
    
    contEnd = np.where(displ<=interPt)[0][-1]+1
    freeStart = contEnd
    
    contZ = displ[:contEnd]
    freeZ = displ[freeStart:]
    contF = contZ*contFit[0]+contFit[1]
    freeF = freeZ*freeFit[0]+freeFit[1]

    realZ = displ[contEnd]
    realF = force[contEnd]
    
    ctPoint = [realZ,realF] if realCntPt else [interPt,sForce[contGoodL[1]]]
    
    allFit = [contF,freeF]
    
    contB = almost(contFit[0],k,thPc)
    freeB = almost(freeFit[0],0.0,thPc,1,-1)
    valid = contB and freeB
    
    return allFit, ctPoint, valid
      
   
def findJumps(data,multiplierPc):
    meanDiff = np.mean(abs(data[1:]-data[:-1]))
    thr = meanDiff*multiplierPc
    jumps = []
    for i in xrange(data.shape[0]-1):
        if abs(data[i]-data[i+1])>thr:
            jumps.append([i,data[i]])
    return np.array(jumps)


def findUnD(data,xAxis,thrMul,distPc,verify=True,rsqT=0.8):
    thr = np.var(data)*thrMul*(-1)
    dist = (xAxis[-1]-xAxis[0])*distPc/100
    uNd = []
    up = None
    down = None
    
    for i in xrange(data.shape[0]-1):
        if data[i+1] <= thr and down == None:
            down = i+1 if data[i] >= thr else None
        elif data[i+1] > thr and down != None:
            up = i+1
            if (xAxis[up]-xAxis[down]) >= dist:
                if verify:
                    fit = genericFit(np.arange(up-down),data[down:up],2)
                    go = fit['R^2']>=rsqT
                else:
                    go = True
                if go:
                    uNd.append([int(down),int(up)])
            down = None
            up = None
            
    return uNd,thr


def polishedDerive(data,sgfWinPcF,sgfWinPcG,sgfDeg,cut = False):
    
    fg = smartSgf(data,sgfWinPcF,sgfDeg)
    fg = np.gradient(fg)
    fgross = smartSgf(data,sgfWinPcG,sgfDeg)
    fgross = np.gradient(fgross)
    f = fg-fgross
    
    start = 0
    end = f.shape[0]
    
    if cut:
        start = end*sgfWinPcF/100/2
        end = f.shape[0]-start
    
    return f,start,end


def peakFinder(segment,sgfWinPcF,sgfWinPcG,sgfDeg,cut,thrMul,distPc,verify,rsqT):
    
    f = segment.f
    z = segment.z
    der,start,end = polishedDerive(f, sgfWinPcF, sgfWinPcG, sgfDeg, cut)
    fnew = f[start:end]
    znew = f[start:end]
    derNew = der[start:end]
    uNd,thr = findUnD(derNew, znew, thrMul, distPc, verify, rsqT)
    peaks = []
    zPeaks = []
    derPeaks = []
    last = 0
    for u in uNd:
        fSlice = fnew[u[0]:u[1]]
        maxPind = np.where(fSlice==np.max(fSlice))[0]
        if u[0]==last:
            first = u[0]
        else:
            base = np.mean(fSlice[maxPind+1:u[1]])
            valleyInd = np.where(fnew[start:maxPind]<=base)[-1]
            if not valleyInd:
                first = last+1
            else:
                first = valleyInd
        peaks.append(fnew[first,u[1]])
        zPeaks.append(znew[first,u[1]])
        derPeaks.append(derNew[first,u[1]])
        last = u[1]
    return peaks,zpeaks,derPeaks


def smartSgf(data,sgfWinPc,sgfDeg,sgfDerDeg = 0):
    
    sgfWin = data.shape[0]*sgfWinPc/100 + 1 - (data.shape[0]*sgfWinPc/100)%2
    filtered = sgf(data,sgfWin,sgfDeg, deriv = sgfDerDeg)
    
    return filtered


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
    