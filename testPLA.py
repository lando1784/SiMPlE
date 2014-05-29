import matplotlib

matplotlib.interactive( True )
matplotlib.use('WXAgg')

import pla
import experiment
import curve
import segment
from platest_conPolyfit import *
import myPla
import myPeakDet as mpd

import os #di sistema
import sys # di sistema
import wx # ok
from wx import Point
import numpy as np
import platform
from os import listdir
from os import walk
from os.path import isfile, join
import matplotlib.pyplot as plt


class MainFrame(wx.Frame):

    def onOpen(self, event=None, altDir = None):
        
        openFileDialog = wx.FileDialog(self, "Open", "", "", 
                                       "All files (*.*)|*.*",
                                       wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
            

        self.curvePath = openFileDialog.GetPath()
        
        self.curve = curve.curve(self.curvePath)
        #self.curve.look()
        plaS = self.curve[-1].getPLA()
        self.CP = [plaS[-1][0],plaS[-1][1]]
        startS = np.where(self.curve[-1].z == self.CP[0])
        startS = 0#startS[0][0]
        self.segments = []
        self.p0 = []
        self.p1 = []
        self.dSeg = []
        
        self.PLAobj = []
        
        for s in self.curve.segments:
            data = np.array([s.z,s.f])
            if np.shape(data)[1] < startS:
                pStart = 0
            else:
                pStart = startS
                #pStart = 0
            seg,p,dSeg = myPla.mySlidingWindow(data[:,pStart:],5000)
            self.segments.append(seg)
            self.p0.append(p)
            self.dSeg.append(dSeg)
            self.PLAobj.append(myPla.PLA(myPla.mySlidingWindow_2,data,5000))
            
        for i in range(len(self.PLAobj[-1].ACs)):
            print self.PLAobj[-1].getSeg(i)['start']
            print self.PLAobj[-1].getSeg(i)['end']

        self.peaks,self.peakInd = mpd.findPeak_Triangle(self.p0[-1],self.dSeg[-1])
        self.peaks2, self.peakInd2 = mpd.findPeak_Greater(self.p0[-1],self.dSeg[-1])
        print self.peakInd
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        if len(self.peakInd)>0:
            ax1.plot(self.curve.segments[-1].z[0::2],self.curve.segments[-1].f[0::2],self.segments[-1][0][0::2],self.segments[-1][1][0::2],'r.',(plaS[0][0],plaS[0][2]),(plaS[0][1],plaS[0][3]),'k--',self.curve.segments[-1].z[self.peakInd],self.curve.segments[-1].f[self.peakInd],'k+',self.curve.segments[-1].z[self.peakInd2],self.curve.segments[-1].f[self.peakInd2],'gx')
        else:
            ax1.plot(self.curve.segments[-1].z[0::2],self.curve.segments[-1].f[0::2],self.segments[-1][0][0::2],self.segments[-1][1][0::2],'r.',(plaS[0][0],plaS[0][2]),(plaS[0][1],plaS[0][3]),'k--')
        fig1.show()
        
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)
        ax2.plot(self.segments[-1][0][0::2],self.dSeg[-1][0::2])
        fig2.show()
            
    def createMenu(self):

        menuBar = wx.MenuBar()
        menuFile = wx.Menu()
        menu1 = wx.Menu()
        self.openFiles = menu1.Append(wx.ID_ANY, "&Open", "This the text in the Statusbar")
        self.Bind(wx.EVT_MENU, self.onOpen, self.openFiles)
        menuBar.Append(menu1, "&File")
        self.SetMenuBar(menuBar)
        

    def __init__(self):
        wx.Frame.__init__(self, None, title = "Prova PLA" , size=(300, 150), style = wx.DEFAULT_FRAME_STYLE)#, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.createMenu()
        self.Layout()
        
        
if __name__ == '__main__':
    wx.SetDefaultPyEncoding('utf8') 
    myapp = wx.App(redirect=False)
    
    mf = MainFrame()
    mf.Show()
    mf.CenterOnScreen()
    
    myapp.MainLoop()