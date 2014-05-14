import experiment
from savitzky_golay import *
import numpy as np

import pla as segment
import fit

from matplotlib.pylab import gca, figure, plot, subplot, title, xlabel, ylabel, xlim,show
from matplotlib.lines import Line2D

c = experiment.experiment()
c.addDirectory('./datas/')

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
    segments = segment.bottomupsegment(data, fit.interpolate, fit.sumsquared_error, max_error)
    draw_plot(data,"Bottom-up with simple interpolation")
    draw_segments(segments)
    
    #top-down with  simple interpolation
    figure()
    segments = segment.topdownsegment(data, fit.interpolate, fit.sumsquared_error, max_error)
    draw_plot(data,"Top-down with simple interpolation")
    draw_segments(segments)
    
    
    show()