from scipy.optimize import leastsq,curve_fit
from numpy.linalg import solve
import numpy as np


def genericFit(x,y,model=1,p0=None,logMe = False):
    
    if logMe:
        x = np.log(x)
        y = np.log(y)
    
    if type(model)==int:
        fitP = (np.polyfit(x,y,model))
        fit = applyPolyModel(x,fitP)
        rsq = RsqPoly(x,y,fitP)
    else:
        fitP = (curve_fit(model,x,y,p0))[0]
        fit = model(x,*fitP)
        rsq = Rsq(x,y,model,fitP)
        
    return {'fitParams':fitP,'fit':fit,'R^2':rsq}


def applyPolyModel(x,params):
    
    y = np.zeros(x.shape)
    e = params.shape[0]-1
    
    for p in params:
        y += x**(e)*p
        e -= 1
        
    return y


def SSRpoly(x,y,params):
    
    yM = applyPolyModel(x,params)
    SSR = np.sum((y-yM)**2)
    
    return SSR


def SSR(model,x,y,par):
    
    yM = model(x,*par)
    
    SSR = np.sum((y-yM)**2)
    
    return SSR


def SST(data):
    
    return np.sum((data-np.mean(data))**2)


def RsqPoly(x,y,params):
    
    ssr = SSRpoly(x,y,params)
    sst = SST(y)
    
    Rsq = 1-(ssr/sst)
    
    return Rsq


def Rsq(x,y,model,params):
    
    ssr = SSR(model,x,y,params)
    sst = SST(y)
    
    Rsq = 1-(ssr/sst)
    
    return Rsq