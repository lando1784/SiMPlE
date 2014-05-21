import experiment
from savitzky_golay import *
import numpy as np

import pla
import fit

import platest
import pla as segment

from matplotlib.pylab import gca, figure, plot, subplot, title, xlabel, ylabel, xlim,show, savefig
from matplotlib.lines import Line2D

from scipy.stats.distributions import t

#c = experiment.experiment()
#c.addDirectory('./datas/')

def idea1(curva,deg=1,size=500):
    if len(curva)<2:
        print "BAD curve"
        return
    
    z = curva[-1].z
    f = curva[-1].f
    k = curva.k
    segments = pla.topdownsegment(f/k, fit.regression, fit.sumsquared_error, size)
        
    s = segments[-1]
    i1 = s[0]
    i2 = s[2]
    xdata = z[i1:i2]
    ydata = f[i1:i2]        
    pdata = np.polyfit(xdata, ydata, deg)    
    plot(z,f,'r-')
    plot(z[i1:i2],f[i1:i2],'c-')
    plot(z,np.polyval(pdata,z),'k--')

def segmenta(curva,deg=3,size=1000,doFit=False):
    if len(curva)<2:
        print "BAD curve"
        return
    
    z = curva[-1].z
    f = curva[-1].f
    k = curva.k
    segments = pla.topdownsegment(f/k, fit.regression, fit.sumsquared_error, size)

    if doFit:
        polynomes = []
        
        for s in segments:
            i1 = s[0]
            i2 = s[2]
            
            xdata = z[i1:i2]
            ydata = f[i1:i2]
            
            pdata = np.polyfit(xdata, ydata, deg)
            
            polynomes.append([xdata,np.polyval(pdata,xdata)])

    for i in range(len(segments)):
        i1 = segments[i][0]
        i2 = segments[i][2]
        if doFit:
            p = polynomes[i]
        if i%2 == 0:
            plot(z[i1:i2],f[i1:i2],'r-')
            if doFit:
                plot(p[0],p[1],'b-')                
        else:
            plot(z[i1:i2],f[i1:i2],'g-')
            if doFit:
                plot(p[0],p[1],'k-')
        i+=1    

def prova(deg=3,fname='./datas/AFS2_crv10pt1.txt',size=1000,doFit=False):
    curva = experiment.curve.curve(fname)
    if len(curva)<2:
        print "BAD curve"
        return
    
    curva[2].setCurve()
    z,f = curva[2].getRelevant()
    k = curva.k
    segments = pla.topdownsegment(f/k, fit.regression, fit.sumsquared_error, size)

    if doFit:
        polynomes = []
        
        for s in segments:
            i1 = s[0]
            i2 = s[2]
            
            xdata = z[i1:i2]
            ydata = f[i1:i2]
            
            pdata = np.polyfit(xdata, ydata, deg)
            
            polynomes.append([xdata,np.polyval(pdata,xdata)])

    for i in range(len(segments)):
        i1 = segments[i][0]
        i2 = segments[i][2]
        if doFit:
            p = polynomes[i]
        if i%2 == 0:
            plot(z[i1:i2],f[i1:i2],'r-')
            if doFit:
                plot(p[0],p[1],'b-')                
        else:
            plot(z[i1:i2],f[i1:i2],'g-')
            if doFit:
                plot(p[0],p[1],'k-')
        i+=1    
                    
#deprecated###################
def outliers(array, num_max): # array and maximum number of outliers
    n = len(array)
    R, Lambda , maxm = [], [], []
    for i in xrange(num_max + 1):
        #xmean = array.mean()
        xmean=sum(array) / float(len(array))
        #xstd  = array.std()
        xstd=np.std(array)
        max_dev = np.abs((array - xmean)/xstd) # Maximum deviation
        maxm.append(np.argmax(max_dev))
        R.append(max_dev[maxm[-1]])
        p = 1.0 - 0.05/(2.0*(n - i + 1)) #problema su questa: float division by zero
        crit = t.ppf(p, n-i-1)
        Lambda.append((n-i)*crit / np.sqrt((n-i-1+crit**2) * (n-i+1)))
    ofound = False
    for j in xrange(num_max-1, -1, -1):
        if R[j] > Lambda[j]:
            ofound = True
        break
    if ofound:
        return j+1, maxm[0:j+1]
##############################
        
        


def draw_plot(data,plot_title):
    plot(range(len(data)),data,alpha=0.8,color='red')
    title(plot_title)
    xlabel("Samples")
    ylabel("Signal")
    xlim((0,len(data)-1))

def draw_segments(segments):
    print 'drawing'
    ax = gca()
    for segment in segments:
        line = Line2D((segment[0],segment[2]),(segment[1],segment[3]))
        ax.add_line(line)

def draw_regions(segments,mini,maxi):
    ax = gca()
    for segment in segments:
        line = Line2D((segment[0],segment[0]),(mini,maxi),linestyle='--')
        line = Line2D((segment[2],segment[2]),(mini,maxi),linestyle='--')
        ax.add_line(line)

def proregion(data, max_error = 0.005):    
    #sliding window with regression
    figure()
    
    mini = min(data)
    maxi = max(data)
    
    segments = segment.slidingwindowsegment(data, fit.regression, fit.sumsquared_error, max_error)
    draw_plot(data,"Sliding window with regression")
    draw_regions(segments,mini,maxi)
    
    #bottom-up with regression
    figure()
    segments = segment.bottomupsegment(data, fit.regression, fit.sumsquared_error, max_error)
    draw_plot(data,"Bottom-up with regression")
    draw_regions(segments,mini,maxi)
    
    #top-down with regression
    figure()
    segments = segment.topdownsegment(data, fit.regression, fit.sumsquared_error, max_error)
    draw_plot(data,"Top-down with regression")
    draw_regions(segments,mini,maxi)
    
    
    
    #sliding window with simple interpolation
    figure()
    segments = segment.slidingwindowsegment(data, fit.interpolate, fit.sumsquared_error, max_error)
    draw_plot(data,"Sliding window with simple interpolation")
    draw_regions(segments,mini,maxi)
    
    #bottom-up with  simple interpolation
    figure()
    segments = segment.bottomupsegment(data, fit.interpolate, fit.sumsquared_error, max_error)
    draw_plot(data,"Bottom-up with simple interpolation")
    draw_regions(segments,mini,maxi)
    
    #top-down with  simple interpolation
    figure()
    segments = segment.topdownsegment(data, fit.interpolate, fit.sumsquared_error, max_error)
    draw_plot(data,"Top-down with simple interpolation")
    draw_regions(segments,mini,maxi)
    
    
    show()

def process(data, max_error = 0.005):    
    #sliding window with regression
    #figure()
    #segments = segment.slidingwindowsegment(data, fit.regression, fit.sumsquared_error, max_error)
    #draw_plot(data,"Sliding window with regression")
    #draw_segments(segments)
    
    #bottom-up with regression
    #figure()
    #segments = segment.bottomupsegment(data, fit.regression, fit.sumsquared_error, max_error)
    #draw_plot(data,"Bottom-up with regression")
    #draw_segments(segments)
    
    #top-down with regression
    figure()
    segments = segment.topdownsegment(data, fit.regression, fit.sumsquared_error, max_error)
    draw_plot(data,"Top-down with regression")
    draw_segments(segments)
    
    #sliding window with simple interpolation
    #figure()
    #segments = segment.slidingwindowsegment(data, fit.interpolate, fit.sumsquared_error, max_error)
    #draw_plot(data,"Sliding window with simple interpolation")
    #draw_segments(segments)
    
    #bottom-up with  simple interpolation
    #figure()
    #segments = segment.bottomupsegment[27][2].t(data, fit.interpolate, fit.sumsquared_error, max_error)
    #draw_plot(data,"Bottom-up with simple interpolation")
    #draw_segments(segments)
    
    #top-down with  simple interpolation
    #figure()
    #segments = segment.topdownsegment(data, fit.interpolate, fit.sumsquared_error, max_error)
    #draw_plot(data,"Top-down with simple interpolation")
    #draw_segments(segments)
    
    
    show()
