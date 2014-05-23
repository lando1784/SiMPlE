import matplotlib

matplotlib.interactive( True )
matplotlib.use('WXAgg')

import pla
import experiment
import curve
import segment
from platest_conPolyfit import *
import myPla

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
        self.curve.look()
        self.segments = []
        self.p0 = []
        self.p1 = []
        self.dSeg = []
        
        for s in self.curve.segments:
            data = np.array([s.z,s.f])
            seg,p,dSeg = myPla.mySlidingWindow(data,7500)
            self.segments.append(seg)
            self.p0.append(p[:,0]*1000)
            self.p1.append(p[:,1])
            self.dSeg.append(dSeg)

        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        ax1.plot(self.curve.segments[-1].z[0::2],self.curve.segments[-1].f[0::2],self.segments[-1][0][0::2],self.segments[-1][1][0::2],'r.')
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