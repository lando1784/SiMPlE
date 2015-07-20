from PyQt4 import QtCore, QtGui
from scipy.signal._savitzky_golay import savgol_filter
from copy import copy,deepcopy

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

import os as os
import sys
import pyqtgraph as pg
import numpy as np
import Ui_qtView as qtView_face
from os import makedirs
from os.path import split, join, splitext, exists
from shutil import rmtree
from time import strftime
from cursor import cursor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

#from SiMPlE import experiment
import experiment
import convertR9module as r9
from calc_utilities import *

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

htmlpre = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><style type="text/css">\np, li { white-space: pre-wrap; }\n</style></head><body style=" font-family:"Ubuntu"; font-size:11pt; font-weight:400; font-style:normal;">\n<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">'
htmlpost = '</span></p></body></html>'

compWinPc = 10
sgfWinPc = 10
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
        self.alignFlags = []
        self.ctPoints = []
        self.bad = []
        
        self.exp = experiment.experiment()
        
        logString = 'Welcome!\n'
        self.simpleLogger(logString)


    def addFiles(self, fnames = None):
        if fnames == None:
            fnames = QtGui.QFileDialog.getOpenFileNames(self, 'Select files', './')
        QtCore.QCoreApplication.processEvents()
        pmax = len(fnames)

        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtGui.QProgressDialog("Opening files...", "Cancel opening", 0, pmax);
        i=0
        for fname in fnames:
            logString = 'Loading file {0}\n'.format(fname)
            self.simpleLogger(logString)
            QtCore.QCoreApplication.processEvents()
            self.exp.addFiles([str(fname)])
            progress.setValue(i)
            i=i+1
            self.alignFlags.append(False)
            if (progress.wasCanceled()):
                break
            self.ctPoints.append(None)
        progress.setValue(pmax)
        QtGui.QApplication.restoreOverrideCursor()

        self.curveRelatedEnabling(True)

        self.refillList()
        self.goToCurve(1)


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
        logString = 'Loading curves from {0}\n'.format(dirname)
        self.simpleLogger(logString)
        for fnamealone in loadedFiles:
            #if i % 100 == 0:
            if fnamealone[0]=='.':
                continue
            QtCore.QCoreApplication.processEvents()
            fname = os.path.join(str(dirname), fnamealone)
            try:
                self.exp.addFiles([str(fname)])
                self.alignFlags.append(False)
                self.ctPoints.append(None)
            except Exception as e:
                print e.message
                
            progress.setValue(i)
            i=i+1
            if (progress.wasCanceled()):
                break
        progress.setValue(pmax)
        QtGui.QApplication.restoreOverrideCursor()
        logString = 'Curves Loaded\n'
        self.simpleLogger(logString)
        
        self.curveRelatedEnabling(True)
        
        self.refillList()
        self.goToCurve(1)


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
        og = self.ui.griglia.items()
        for i in range(len(og)):
            if not self.exp[-i-1].relevant:
                og[i].setBrush(self.cRosso)
                og[i].setPen(self.cRosso)
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
        print 'dove-1 ' + str(dove-1)
        print 'len ' + str(len(self.exp)) 
        if len(self.exp)<=dove-1 or dove-1<0:
            return None
        else:
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
        start = 1 if self.alignFlags[dove] else 0
        self.ui.alignBtn.setEnabled(not self.alignFlags[dove])
        self.ui.alignAllBtn.setEnabled(not np.array(self.alignFlags).all())
        self.ui.autoFitBtn.setEnabled(not self.alignFlags[dove] and not self.fitFlag)
        self.ui.rejectBtn.setEnabled(not self.alignFlags[dove] and self.fitFlag)
        self.ui.removeBOBtn.setEnabled(len(self.bad)>=1)
        self.ui.saveBtn.setEnabled(self.alignFlags[dove])
        self.ui.saveAllBtn.setEnabled(self.alignFlags[dove])
        for p in self.exp[dove][start:]:
            if p == self.exp[dove][-1]:
                self.ui.grafo.plot(p.z,p.f,pen='b')
            else:
                self.ui.grafo.plot(p.z,p.f)
        if self.fitFlag:
            self.plotDeriv(-1)
            self.cursor = cursor(self.ui.grafo.plotItem,1,True,True,'o','m')
        if self.alignFlags[dove]:
            self.ui.grafo.plotItem.addLine(x=0)
            self.ui.grafo.plotItem.addLine(y=0)
        if autorange:
            self.ui.grafo.autoRange()
            
    
    def batchConv(self):
        
        dirIn = str(QtGui.QFileDialog.getExistingDirectory(self, 'Select a directory', './'))
        DirIn = split(dirIn)
        dirOut = join(DirIn[0],'jpk_'+DirIn[1])
        r9.batchR9conversion(dirIn,dirOut)
        rmtree(dirIn)
        logString = 'Converted R9 files from {0} to JPK txt files in directory {1}\n'.format(dirIn,dirOut)
        self.simpleLogger(logString)
        self.addDirectory()


    def updateK(self):
        
        culprit = self.sender()
        currIndex = self.ui.slide1.value()
        k = self.ui.kNumDbl.value()*1000
        if culprit is self.ui.updateKBtn:
            logString = 'K value for {0} changed\n'.format(self.exp[currIndex].basename)
            self.simpleLogger(logString)
            self.exp[currIndex].changeK(k)
        else:
            for c in self.exp:
                logString = 'K value for {0} changed\n'.format(c.basename)
                self.simpleLogger(logString)
                c.changeK(k)
            

    def updateSens(self):
        
        culprit = self.sender()
        currIndex = self.ui.slide1.value()
        nmV = self.ui.nmVNumDbl.value()
        if culprit is self.ui.updateNmVBtn:
            logString = 'Nm/V value for {0} changed\n'.format(self.exp[currIndex].basename)
            self.simpleLogger(logString)
            self.exp[currIndex].changeSens(nmV)
        else:
            for c in self.exp:
                logString = 'Nm/V value for {0} changed\n'.format(c.basename)
                self.simpleLogger(logString)
                c.changeSens(nmV)
                
    
    def updateSpeed(self):
        
        culprit = self.sender()
        currIndex = self.ui.slide1.value()
        speed = self.ui.speedNumDbl.value()
        if culprit is self.ui.updateSpeedBtn:
            logString = 'Speed value for {0} changed\n'.format(self.exp[currIndex].basename)
            self.simpleLogger(logString)
            self.exp[currIndex].changeSpeed(speed)
        else:
            for c in self.exp:
                logString = 'Speed value for {0} changed\n'.format(c.basename)
                self.simpleLogger(logString)
                c.changeSpeed(speed)
                
    
    def startAutoFit(self):
        
        self.plotDeriv(-1)
        self.ui.autoFitBtn.setEnabled(False)
        self.ui.rejectBtn.setEnabled(True)
       
    
    def rejectAlign(self):
        
        self.fitFlag = False
        self.goToCurve(self.ui.slide1.value())
        for i in xrange(len(self.exp)):
            self.ctPoints[i] = None
        
    
    def plotDeriv(self,segInd):
        try:
            c = self.exp[self.ui.slide1.value()-1]
            fit, ctPt,_ = fitCnNC(c[segInd],'>',sgfWinPc,sgfDeg,compWinPc,winged = False,wingPc = 0, thPc = self.ui.slopePcNum.value())
            if self.ctPoints[self.ui.slide1.value()-1] == None:
                self.ctPoints[self.ui.slide1.value()-1] = ctPt
            self.ui.grafo.plot(self.ui.grafo.plotItem.curves[segInd].xData,fit,pen='r')
            self.ui.grafo.plot([ctPt[0]],[ctPt[1]], symbol = 'o',symbolPen = 'g',symbolBrush = 'g')
            self.fitFlag = True
        except Exception as e:
            print e.message
            
    
    def align(self):
        culprit = self.sender()
        self.fitFlag = False
        if culprit is self.ui.alignBtn:
            try:
                logString = 'Aligning {0}\n'.format(self.exp[self.ui.slide1.value()-1].basename)
                self.simpleLogger(logString)
                _,contactPt, valid = fitCnNC(self.exp[self.ui.slide1.value()-1][-1],'>',sgfWinPc,sgfDeg,compWinPc,
                                             winged = False,wingPc = 0, thPc = self.ui.slopePcNum.value())
                if self.ctPoints[self.ui.slide1.value()-1] != None:
                    contactPt = self.ctPoints[self.ui.slide1.value()-1]
                    self.ctPoints[self.ui.slide1.value()-1] = None
                    
                for s in self.exp[self.ui.slide1.value()-1][1:]:
                    s.f = s.f[np.where(s.z>=contactPt[0])]-contactPt[1]
                    s.z = s.z[np.where(s.z>=contactPt[0])]-contactPt[0]
                self.exp[self.ui.slide1.value()-1].relevant = valid
                if not valid:
                    self.bad.append(self.ui.slide1.value()-1)
                self.alignFlags[self.ui.slide1.value()-1] = True
                self.goToCurve(self.ui.slide1.value())
                self.ui.slide1.setValue(self.ui.slide1.value())
                self.ui.slide2.setValue(self.ui.slide1.value())
            except Exception as e:
                print e.message
        else:
            pmax = len(self.exp)
            logString = 'Aligning all curves...\n'
            self.simpleLogger(logString)
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            progress = QtGui.QProgressDialog("Aligning curves...", "Cancel aligning", 0, pmax);
            i=0
            for c in self.exp:
                progress.setValue(i)
                if (progress.wasCanceled()):
                    break
                if self.alignFlags[i]:
                    i=i+1
                    continue
                try:
                    _,contactPt,valid = fitCnNC(c[-1],'>',sgfWinPc,sgfDeg,compWinPc,winged = False,wingPc = 0, 
                                                thPc = self.ui.slopePcNum.value())
                    if self.ctPoints[i] != None:
                        contactPt = self.ctPoints[i]
                        self.ctPoints[i] = None
                    c.relevant = valid
                    if not valid:
                        self.bad.append(i)
                        
                    for s in c[1:]:
                        s.f = s.f[np.where(s.z>=contactPt[0])]-contactPt[1]
                        s.z = s.z[np.where(s.z>=contactPt[0])]-contactPt[0]
                except Exception as e:
                    print e.message
                self.alignFlags[i] = True
                i=i+1
            progress.setValue(pmax)
            QtGui.QApplication.restoreOverrideCursor()
            logString = 'Curves aligned\n'
            self.simpleLogger(logString)
            self.goToCurve(1)
            self.ui.slide1.setValue(0)
            self.ui.slide2.setValue(0)
        self.refillList()


    def reload(self):
        pmax = len(self.exp)
        self.bad = []
        self.ui.removeBOBtn.setEnabled(False)
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        logString = 'Reloading all the curves\n'
        self.simpleLogger(logString)
        progress = QtGui.QProgressDialog("Reloading curves...", "Cancel reloading", 0, pmax);
        i=0
        tempExp = deepcopy(self.exp)
        self.exp = None
        self.exp = experiment.experiment()
        for c in tempExp:
            self.alignFlags[i]=False
            self.ctPoints [i] = None
            i+=1
            progress.setValue(i)
            self.exp.addFiles([c.filename])
        progress.setValue(pmax)
        QtGui.QApplication.restoreOverrideCursor()
        tempExp = None
        self.fitFlag = False
        self.refillList()
        self.goToCurve(1)
        self.ui.slide1.setValue(0)
        self.ui.slide2.setValue(0)
        logString = 'Curves reloaded\n'
        self.simpleLogger(logString)
        
        
    def saveAligned(self):
        
        if self.sender() is self.ui.saveBtn:
            ind = self.ui.slide1.value()-1
            c = self.exp[ind]
            if not self.alignFlags[ind] or len(c)<1:
                return None
            cc = deepcopy(c)
            dir = join(split(c.filename)[0],'aligned')
            logString = 'Saving {0} aligned version in {1}\n'.format(c.basename,dir)
            self.simpleLogger(logString)
            if not exists(dir):
                makedirs(dir)
            onlyFile,ext = splitext(c.basename)
            if cc[0].direction == 'near':
                del cc[0]
            basename = onlyFile+'_aligned'+ext
            filename = join(dir,basename)
            cc.save(filename)
            cc = None
        else:
            for i in xrange(len(self.exp)):
                c = self.exp[i]
                if not self.alignFlags[i] or len(c)<1:
                    continue
                cc = deepcopy(c)
                dir = join(split(c.filename)[0],'aligned')
                logString = 'Saving {0} aligned version in {1}\n'.format(c.basename,dir)
                self.simpleLogger(logString)
                if not exists(dir):
                    makedirs(dir)
                onlyFile,ext = splitext(c.basename)
                if cc[0].direction == 'near':
                    del cc[0]
                basename = onlyFile+'_aligned'+ext
                filename = join(dir,basename)
                cc.save(filename)
                cc = None
        

    def simpleLogger(self,entry):
        completeEntry = strftime('%Y/%m/%d') + '-' + strftime('%H:%M:%S') + ' -- ' + entry
        self.ui.logTxt.insertPlainText(completeEntry)
        
        
    def removeCurve(self):
        culprit = self.sender()
        if culprit.text() == 'Remove Curve' or culprit.text() == 'Remove bad ones':
            culprit.setText('REALLY?')
            return None
        elif culprit is self.ui.removeBtn:
            ind = self.ui.slide1.value()-1
            logString = '{0} Removed\n'.format(self.exp[ind].basename)
            self.simpleLogger(logString)
            del self.exp[ind]
            del self.alignFlags[ind]
            del self.ctPoints[ind]
            culprit.setText('Remove Curve')
            if len(self.exp)<1:
                self.curveRelatedEnabling(False)
                self.ui.grafo.clear()
            else:
                self.goToCurve(1)
        else:
            tempExp = [k for j, k in enumerate(self.exp) if j in self.bad]
            for t in tempExp:
                logString = '{0} Removed\n'.format(t.basename)
                self.simpleLogger(logString)
                del self.exp[t.basename]
            self.alignFlags = [k for j, k in enumerate(self.alignFlags) if j not in self.bad]
            self.ctPoints = [k for j, k in enumerate(self.ctPoints) if j not in self.bad]
            culprit.setText('Remove bad ones')
            self.bad = []
            self.ui.removeBOBtn.setEnabled(False)
            if len(self.exp)<1:
                self.curveRelatedEnabling(False)
                self.ui.grafo.clear()
            else:
                self.goToCurve(1)
                
        
        self.refillList()
        
    
    def curveRelatedEnabling(self,value):
        
        self.ui.kNumDbl.setEnabled(value)
        self.ui.nmVNumDbl.setEnabled(value)
        self.ui.speedNumDbl.setEnabled(value)
        self.ui.updateKBtn.setEnabled(value)
        self.ui.updateNmVBtn.setEnabled(value)
        self.ui.updateSpeedBtn.setEnabled(value)
        self.ui.updateAllKBtn.setEnabled(value)
        self.ui.updateAllNmVBtn.setEnabled(value)
        self.ui.updateAllSpeedBtn.setEnabled(value)
        self.ui.reloadBtn.setEnabled(value)
        self.ui.slopePcNum.setEnabled(value)
        self.ui.alignAllBtn.setEnabled(value)
        self.ui.removeBtn.setEnabled(value)


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
        QtCore.QObject.connect(self.ui.rejectBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.rejectAlign)
        QtCore.QObject.connect(self.ui.alignBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.align)
        QtCore.QObject.connect(self.ui.alignAllBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.align)
        QtCore.QObject.connect(self.ui.reloadBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.reload)
        QtCore.QObject.connect(self.ui.saveBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.saveAligned)
        QtCore.QObject.connect(self.ui.saveAllBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.saveAligned)
        QtCore.QObject.connect(self.ui.removeBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.removeCurve)
        QtCore.QObject.connect(self.ui.removeBOBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.removeCurve)
        
        
        
        
        
        QtCore.QMetaObject.connectSlotsByName(self)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName( 'qtView' )
    canale = curveWindow()
    canale.show()
    QtCore.QObject.connect( app, QtCore.SIGNAL( 'lastWindowClosed()' ), app, QtCore.SLOT( 'quit()' ) )
    sys.exit(app.exec_())