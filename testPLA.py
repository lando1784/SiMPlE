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
        print np.shape(self.curve.segments[0].z)
        print np.shape(self.curve.segments[1].z)
        print np.shape(self.curve.segments[2].z)
        
        for s in self.curve.segments:
            data = np.array([s.z,s.f])
            seg,p = myPla.mySlidingWindow(data,500)
            self.segments.append(seg)
        
        print self.segments
        print np.shape(self.segments[0])
        print np.shape(self.segments[1])
        print np.shape(self.segments[2])
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        
        ax1.plot(self.curve.segments[2].z[0:3700:100],self.curve.segments[2].f[0:3700:100],self.curve.segments[2].z[0:3700:100],self.segments[2][0:3700:100])
        
        fig1.show()
            
        
            
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