import experiment
from savitzky_golay import *
import numpy as np

import pla as segment
import fit

from matplotlib.pylab import gca, figure, plot, subplot, title, xlabel, ylabel, xlim,show
from matplotlib.lines import Line2D

#c = experiment.experiment()
#c.addDirectory('./datas/')

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
def getmq(seg):
    dy = seg[3]-seg[1]
    dx = seg[2]-seg[0]
    m = dy/dx
    q = seg[3]-m*seg[2]
    return m,q

def draw_plot(data,plot_title):
    plot(range(len(data)),data,alpha=0.8,color='red')
    title(plot_title)
    xlabel("Samples")
    ylabel("Signal")
    xlim((0,len(data)-1))

def draw_segments(segments):
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
    figure()
    segments = segment.slidingwindowsegment(data, fit.regression, fit.sumsquared_error, max_error)
    draw_plot(data,"Sliding window with regression")
    draw_segments(segments)
    
    #bottom-up with regression
    figure()
    segments = segment.bottomupsegment(data, fit.regression, fit.sumsquared_error, max_error)
    draw_plot(data,"Bottom-up with regression")
    draw_segments(segments)
    
    #top-down with regression
    figure()
    segments = segment.topdownsegment(data, fit.regression, fit.sumsquared_error, max_error)
    draw_plot(data,"Top-down with regression")
    draw_segments(segments)
    
    
    
    #sliding window with simple interpolation
    figure()
    segments = segment.slidingwindowsegment(data, fit.interpolate, fit.sumsquared_error, max_error)
    draw_plot(data,"Sliding window with simple interpolation")
    draw_segments(segments)
    
    #bottom-up with  simple interpolation
    figure()
    segments = segment.bottomupsegmene[27][2].t(data, fit.interpolate, fit.sumsquared_error, max_error)
    draw_plot(data,"Bottom-up with simple interpolation")
    draw_segments(segments)
    
    #top-down with  simple interpolation
    figure()
    segments = segment.topdownsegment(data, fit.interpolate, fit.sumsquared_error, max_error)
    draw_plot(data,"Top-down with simple interpolation")
    draw_segments(segments)
    
    
    show()