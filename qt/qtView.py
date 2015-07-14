from PyQt4 import QtCore, QtGui
from scipy.signal._savitzky_golay import savgol_filter

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

import os as os
import sys
import pyqtgraph as pg
import numpy as np
import Ui_qtView as qtView_face
from os.path import split, join
from shutil import rmtree

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

#from SiMPlE import experiment
import experiment
import convertR9module as r9
from calc_utilities import *
from scipy.signal import savgol_filter as sgf

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

htmlpre = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><style type="text/css">\np, li { white-space: pre-wrap; }\n</style></head><body style=" font-family:"Ubuntu"; font-size:11pt; font-weight:400; font-style:normal;">\n<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">'
htmlpost = '</span></p></body></html>'

compWin = 50
sgfWin = 101
sgfDeg = 3

class curveWindow ( QtGui.QMainWindow ):
    iter = 0
    prev = 0
    cRosso = QtGui.QColor(255,0,0)
    cVerde = QtGui.QColor(50,255,50)
    cNero = QtGui.QColor(0,0,0)
    def __init__ ( self, parent = None ):
        QtGui.QMainWindow.__init__( self, parent )
        self.setWindowTitle( 'qtView' )
        self.ui = qtView_face.Ui_facewindow()
        self.ui.setupUi( self )
        self.setConnections()
        
        self.fitFlag = False

        self.exp = experiment.experiment()


    def addFiles(self, fnames = None):
        if fnames == None:
            fnames = QtGui.QFileDialog.getOpenFileNames(self, 'Select files', './')
        QtCore.QCoreApplication.processEvents()
        pmax = len(fnames)

        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtGui.QProgressDialog("Opening files...", "Cancel opening", 0, pmax);
        i=0
        for fname in fnames:
            QtCore.QCoreApplication.processEvents()
            self.exp.addFiles([str(fname)])
            progress.setValue(i)
            i=i+1
            if (progress.wasCanceled()):
                break
        progress.setValue(pmax)
        QtGui.QApplication.restoreOverrideCursor()

        self.refillList()


    def addDirectory(self,dirname=None):
        if dirname == None:
            dirname = QtGui.QFileDialog.getExistingDirectory(self, 'Select a directory', './')
            if not os.path.isdir(dirname):
                return
        QtCore.QCoreApplication.processEvents()
        pmax = len(os.listdir(dirname))

        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtGui.QProgressDialog("Opening files...", "Cancel opening", 0, pmax);
        i=0
        loadedFiles = sorted(os.listdir(dirname))
        for fnamealone in loadedFiles:
            #if i % 100 == 0:
            QtCore.QCoreApplication.processEvents()
            fname = os.path.join(str(dirname), fnamealone)
            self.exp.addFiles([str(fname)])
            progress.setValue(i)
            i=i+1
            if (progress.wasCanceled()):
                break
        progress.setValue(pmax)
        QtGui.QApplication.restoreOverrideCursor()
        self.refillList()


    def refillList(self):
        scena = QtGui.QGraphicsScene()
        width = self.ui.griglia.width()
        height = self.ui.griglia.height()
        N = len(self.exp)
        self.ui.slide1.setMaximum(N)
        self.ui.slide2.setMaximum(N)
        #self.ui.slide3.setMaximum(N)

        gNx = np.sqrt(N*width/height)
        Nx = int(np.ceil(gNx))
        if int(gNx) == Nx:
            Nx+=1
        L = int(width/Nx)
        i = 0
        j = 0
        k=0
        if L<=3:
            L=3
        while i*Nx+j<N:
            h = L-2
            w = L-2
            
            rect = QtCore.QRectF(j*(L)+1, i*(L)+1, h, w)
            idrect = scena.addRect(rect, pen = QtGui.QPen(self. cVerde,0) ,brush = self. cVerde )
            j+=1
            k+=1
            if j == Nx:
                j=0
                i+=1

        scena.wheelEvent = self.scorri
        self.ui.griglia.setScene(scena)
        self.ui.slide1.setValue(1)
#        og = self.ui.griglia.items()
#        for i in range(len(og)):
#            if self.curves[-i-1].inconsistency:
#                og[i].setBrush(self.cRosso)
#                og[i].setPen(self.cRosso)
        self.ui.griglia.invalidateScene()

        return True
    
    
    def scorri(self,ev=None):
        delta = ev.delta()/120
        self.ui.slide2.setSliderPosition(self.ui.slide2.sliderPosition()-delta)
        
        
    def sqSwitch(self,i,n):
        og = self.ui.griglia.items()
        if n:
            c = self.cNero
        else:
            c = og[-i].brush().color()
        og[-i].setPen(c)
        
        
    def goToCurve(self,dove):
        self.ui.labFilename.setText(htmlpre + self.exp[dove-1].basename + htmlpost)
        if self.prev != 0:
            self.sqSwitch(self.prev,False)
        self.sqSwitch(dove,True)
        self.prev = dove
        self.viewCurve(dove)
        self.ui.kNumDbl.setValue(self.exp[dove-1].k/1000)
        self.ui.nmVNumDbl.setValue(self.exp[dove-1].sensitivity)
        self.ui.speedNumDbl.setValue(self.exp[dove-1][0].speed)


    def updateCurve(self):
        self.viewCurve(self.ui.slide1.value(),autorange=False)
        
        
    def refreshCurve(self):
        self.viewCurve(self.ui.slide1.value(),autorange=True)
        

    def viewCurve(self,dove = 1,autorange=True):
        dove -= 1
        self.ui.grafo.clear()
        for p in self.exp[dove]:
            if p == self.exp[dove][-1]:
                self.ui.grafo.plot(p.z,p.f,pen='b')
            else:
                self.ui.grafo.plot(p.z,p.f)
        if self.fitFlag:
            self.plotDeriv(-1)
        if autorange:
            self.ui.grafo.autoRange()
            
    
    def batchConv(self):
        
        dirIn = str(QtGui.QFileDialog.getExistingDirectory(self, 'Select a directory', './'))
        DirIn = split(dirIn)
        dirOut = join(DirIn[0],'jpk_'+DirIn[1])
        r9.batchR9conversion(dirIn,dirOut)
        rmtree(dirIn)
        self.addDirectory()


    def updateK(self):
        
        culprit = self.sender()
        currIndex = self.ui.slide1.value()
        k = self.ui.kNumDbl.value()*1000
        if culprit is self.ui.updateKBtn:
            self.exp[currIndex].changeK(k)
        else:
            for c in self.exp:
                c.changeK(k)
            

    def updateSens(self):
        
        culprit = self.sender()
        currIndex = self.ui.slide1.value()
        nmV = self.ui.nmVNumDbl.value()
        if culprit is self.ui.updateNmVBtn:
            self.exp[currIndex].changeSens(nmV)
        else:
            for c in self.exp:
                c.changeSens(nmV)
                
    
    def updateSpeed(self):
        
        culprit = self.sender()
        currIndex = self.ui.slide1.value()
        speed = self.ui.speedNumDbl.value()
        if culprit is self.ui.updateSpeedBtn:
            self.exp[currIndex].changeSpeed(speed)
        else:
            for c in self.exp:
                c.changeSpeed(speed)
                
    
    def startAutoFit(self):
        
        self.plotDeriv(-1)
             
        
        
    def startManualSel(self):
        
        culprit = self.sender()
        if culprit.text() == 'Manual selection':
            try:
                att = dir(self.ui.grafo.plotItem.curves[0])
                for a in att:
                    print a
                culprit.setText('Select First NC point')
            except:
                return False
        elif culprit.text() == 'Select First NC point':
            culprit.setText('Select Second NC point')
        elif culprit.text() == 'Select Second NC point':
            culprit.setText('Select First C point')
        elif culprit.text() == 'Select First C point':
            culprit.setText('Select Second C point')
        elif culprit.text() == 'Select Second C point':
            culprit.setText('Apply All')
        else:
            culprit.setText('Manual selection')
        print 'Manual'


    def setPointC(self):
        print 'ciao'
        
    
    def rejectAlign(self):
        
        self.fitFlag = False
        self.goToCurve(0)
        
    
    def plotDeriv(self,segInd):
        try:
            sig = sgf(self.ui.grafo.plotItem.curves[segInd].yData,sgfWin,sgfDeg)
            gradSig = np.gradient(sig)
            gradSqSig = np.gradient(gradSig)
            conf = movingComp(gradSig,0.0,'>',compWin)
            bMask,ranges = WAThBRIF(conf)
            print bMask
            print ranges
            conf2 = conf*(sig[-1]-sig[0])
            dataMasked = conf*sig
            dataMasked[np.where(dataMasked == 0.0)] = sig[-1]
            conf-=np.max(conf)
            conf2-=np.max(conf2)
            self.ui.grafo.plot(self.ui.grafo.plotItem.curves[segInd].xData,dataMasked,pen='r')
            self.fitFlag = True
        except Exception as e:
            print e.message


    def setConnections(self):

        QtCore.QObject.connect(self.ui.slide1, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.ui.slide2.setValue)
        
        QtCore.QObject.connect(self.ui.slide2, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.ui.slide1.setValue)
        
        QtCore.QObject.connect(self.ui.slide1, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.goToCurve )

        QtCore.QObject.connect(self.ui.bAddDir, QtCore.SIGNAL(_fromUtf8("clicked()")), self.addDirectory)
        QtCore.QObject.connect(self.ui.bAddFiles, QtCore.SIGNAL(_fromUtf8("clicked()")), self.addFiles)
        
        QtCore.QObject.connect(self.ui.convr9Btn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.batchConv)
        
        QtCore.QObject.connect(self.ui.updateKBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.updateK)
        QtCore.QObject.connect(self.ui.updateAllKBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.updateK)
        QtCore.QObject.connect(self.ui.updateNmVBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.updateSens)
        QtCore.QObject.connect(self.ui.updateAllNmVBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.updateSens)
        QtCore.QObject.connect(self.ui.updateSpeedBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.updateSpeed)
        QtCore.QObject.connect(self.ui.updateAllSpeedBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.updateSpeed)
        
        QtCore.QObject.connect(self.ui.autoFitBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.startAutoFit)
        QtCore.QObject.connect(self.ui.manSelBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.startManualSel)
        QtCore.QObject.connect(self.ui.rejectBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.rejectAlign)
        
        QtCore.QMetaObject.connectSlotsByName(self)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName( 'qtView' )
    canale = curveWindow()
    canale.show()
    QtCore.QObject.connect( app, QtCore.SIGNAL( 'lastWindowClosed()' ), app, QtCore.SLOT( 'quit()' ) )
    sys.exit(app.exec_())