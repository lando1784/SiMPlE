import pla
import experiment
import curve
import segment
from platest_conPolyfit import *

import os #di sistema
import sys # di sistema
import wx # ok
from wx import Point
import numpy as np
import platform
from os import listdir
from os import walk
from os.path import isfile, join




class MainFrame(wx.Frame):

    def onOpen(self, event=None, altDir = None):
        
        openFileDialog = wx.FileDialog(self, "Open", "", "", 
                                       "All files (*.*)|*.*",
                                       wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
            

        self.curvePath = openFileDialog.GetPath()
        
        self.curve = curve.curve(self.curvePath)
        self.curve.look()
        
        for s in self.curve.segments:
            process(s.f)
      
            
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