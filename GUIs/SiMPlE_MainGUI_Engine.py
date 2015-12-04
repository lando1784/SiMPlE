import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

CURRMOD = list(sys.modules.keys())
try:
    ENV = 'PyQt5'
    CURRMOD.index(ENV)
    from PyQt5.QtWidgets import QMainWindow,QFileDialog,QProgressDialog,QGraphicsScene,QMessageBox,QGraphicsPixmapItem
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QColor,QPixmap,QPen,QCursor
    from PyQt5.QtCore import Qt,QCoreApplication,QRectF,QObject
except:
    ENV = 'PyQt4'
    CURRMOD.index(ENV)
    from PyQt4.QtGui import QColor,QMainWindow,QFileDialog,QApplication,QCursor,QProgressDialog,QGraphicsScene,QPen
    from PyQt4.QtGui import QMessageBox,QPixmap,QGraphicsPixmapItem
    from PyQt4.QtCore import Qt,QCoreApplication,QRectF,QObject,SIGNAL,QMetaObject

from copy import deepcopy

_fromUtf8 = lambda s: s

from PIL import Image

import pyqtgraph as pg
import GUIs.SiMPlE_MainGUI as qtView_face
from os import makedirs
from os.path import split, join, splitext, exists
from shutil import rmtree
from time import strftime

from libs import experiment
from libs import convertR9module as r9
from libs.calc_utilities import *
from libs.cursor import cursor

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

htmlpre = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><style type="text/css">\np, li { white-space: pre-wrap; }\n</style></head><body style=" font-family:"Ubuntu"; font-size:11pt; font-weight:400; font-style:normal;">\n<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">'
htmlpost = '</span></p></body></html>'

compWinPc = 5
sgfWinPc = 2.5
sgfWinPcF = 8
sgfWinPcG = 40
sgfDeg = 3
cutMe = True

MOMCOR = True

line = pg.graphicsItems.InfiniteLine.InfiniteLine

class SiMPlE_main ( QMainWindow ):
    iter = 0
    prev = 0
    cRosso = QColor(255,0,0)
    cVerde = QColor(50,255,50)
    cNero = QColor(0,0,0)
    
    def __init__ ( self, parent = None, verbose = False):
        QMainWindow.__init__( self, parent )
        self.setWindowTitle( 'qtView' )
        self.ui = qtView_face.Ui_facewindow()
        self.ui.setupUi( self )
        self.setConnections()
        
        self.cursColors = {0: ['Magenta','m'],1: ['Cyan','c'],2: ['Green','g'],3:['Black','k']}
        self.cursors = []
        self.ui.cursCmpCmbBox.addItem('Select a cursor')
        
        self.fitFlag = False
        self.alignFlags = []
        self.ctPoints = []
        self.bad = []
        self.badFlags = []
        self.ui.setPathBtn.setStyleSheet('background-color: none')
        self.globDir = ''
        self.peaksOnPlot = False
        self.peaksAlreadyPlotted = False
        self.lastOperation = ''
        
        self.exp = experiment.experiment()
        
        self.statusDict = {1:[[self.ui.bAddDir,self.ui.bAddFiles,self.ui.convr9Btn],
                              [self.ui.reloadBtn,self.ui.saveBox,self.ui.removeBox,self.ui.fromFileBox,
                               self.ui.fitNpeakBox,self.ui.alignBox,self.ui.plotModBox,self.ui.cursorsBox,
                               self.ui.peaksTab]],
                           2:[[self.ui.removeBox,self.ui.removeBtn,self.ui.reloadBtn,self.ui.closeExpBtn,
                               self.ui.fromFileBox,self.ui.fitNpeakBox,self.ui.alignBox,self.ui.plotModBox,
                               self.ui.cursorsBox],
                              [self.ui.removeBOBtn,self.ui.saveBox,self.ui.peaksTab,self.ui.chgStatBtn]],
                           3:[[self.ui.removeBOBtn,self.ui.saveBox,self.ui.peaksTab,self.ui.chgStatBtn,self.ui.findPeaksBtn],
                              [self.ui.showPeakBtn,self.ui.peaksCmbBox,self.ui.alignBox,self.ui.savePeaksBox]],
                           4:[[self.ui.showPeakBtn,self.ui.peaksCmbBox,self.ui.savePeaksBox,self.ui.removeBOBtn],
                              []]}
        
        logString = 'Welcome!\n'
        self.simpleLogger(logString)
        self.setStatus(1)


    def setStatus(self,status):
        
        for act in self.statusDict[status][0]:
            act.setEnabled(True)
            for c in act.children():
                try:
                    c.setEnabled(True)
                except:
                    pass
        for dis in self.statusDict[status][1]:
            dis.setEnabled(False)
            for c in act.children():
                try:
                    c.setEnabled(True)
                except:
                    pass


    def addFiles(self, fnames = None):
        if fnames == False or fnames is None:
            fnames = QFileDialog.getOpenFileNames(self, 'Select files', './')
        QCoreApplication.processEvents()
        pmax = len(fnames)

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        progress = QProgressDialog("Opening files...", "Cancel opening", 0, pmax);
        i=0
        for fname in fnames:
            logString = 'Loading file {0}\n'.format(fname)
            self.simpleLogger(logString)
            QCoreApplication.processEvents()
            self.exp.addFiles([str(fname)])
            if MOMCOR:
                self.exp[-1].sensitivity/=1e9
                self.exp[-1].k/=1000
            if self.exp[-1][0].f.all() == 0 or self.exp[-1][-1].f.all() == 0:
                    del self.exp[-1]
                    continue
            progress.setValue(i)
            i=i+1
            aligned = self.exp[-1][0].direction == 'far'
            self.alignFlags.append(aligned)
            self.badFlags.append(True)
            self.ctPoints.append(None)
            if (progress.wasCanceled()):
                break
        progress.setValue(pmax)
        QApplication.restoreOverrideCursor()
        
        self.setStatus(2)
        if np.array(self.alignFlags).all():
            self.setStatus(3)
        
        self.refillList()
        self.goToCurve(1)


    def addDirectory(self,dirname=None):
        if dirname == False or dirname is None:
            if ENV == 'PyQt4': dirname = QFileDialog.getExistingDirectory(self, 'Select a directory', './')
            else: dirname = QFileDialog.getExistingDirectory(self, 'Select a directory', './')[0]
            if not os.path.isdir(dirname):
                return
        QCoreApplication.processEvents()
        pmax = len(os.listdir(dirname))

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        progress = QProgressDialog("Opening files...", "Cancel opening", 0, pmax);
        i=0
        loadedFiles = sorted(os.listdir(dirname))
        logString = 'Loading curves from {0}\n'.format(dirname)
        self.simpleLogger(logString)
        for fnamealone in loadedFiles:
            #if i % 100 == 0:
            if fnamealone[0]=='.':
                continue
            QCoreApplication.processEvents()
            fname = os.path.join(str(dirname), fnamealone)
            try:
                self.exp.addFiles([str(fname)])
                if self.exp[-1][0].f.all() == 0 or self.exp[-1][-1].f.all() == 0:
                    del self.exp[-1]
                    continue
                aligned = self.exp[-1][0].direction == 'far'
                self.alignFlags.append(aligned)
                self.badFlags.append(True)
                self.ctPoints.append(None)
            except Exception as e:
                print(e.message)
                
            progress.setValue(i)
            i=i+1
            if (progress.wasCanceled()):
                break
        progress.setValue(pmax)
        QApplication.restoreOverrideCursor()
        logString = 'Curves Loaded\n'
        self.simpleLogger(logString)
        
        self.setStatus(2)
        if np.array(self.alignFlags).all():
            self.setStatus(3)
        
        self.refillList()
        self.goToCurve(1)


    def refillList(self,lastInd=1):
        self.ui.curveNameCmbBox.clear()
        self.ui.curveNameCmbBox.addItem('Currently loaded curves:')
        for f in self.exp.basenames:
            self.ui.curveNameCmbBox.addItem(f)
        scena = QGraphicsScene()
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
            
            rect = QRectF(j*(L)+1, i*(L)+1, h, w)
            idrect = scena.addRect(rect, pen = QPen(self. cVerde,0) ,brush = self. cVerde )
            j+=1
            k+=1
            if j == Nx:
                j=0
                i+=1
        
        scena.mouseReleaseEvent = self.aim
        scena.wheelEvent = self.scorri
        self.ui.griglia.setScene(scena)
        og = self.ui.griglia.items()
        for i in range(len(og)):
            if not self.exp[-i-1].relevant:
                og[i].setBrush(self.cRosso)
                og[i].setPen(self.cRosso)
        self.ui.griglia.invalidateScene()
        self.ui.slide1.setValue(lastInd)
        if lastInd == self.ui.slide1.value():
            self.goToCurve(lastInd)

        return True
    
    
    def pointInRect(self,point,rect):
        
        tl = rect.topLeft()
        br = rect.bottomRight()
        
        tlBound = point.x() >= tl.x() and point.y() >= tl.y()
        brBound = point.x() <= br.x() and point.y() <= br.y()
        
        return tlBound and brBound
    
    
    def aim(self,ev=None):
        mPos = ev.scenePos()
        it = self.ui.griglia.items()
        ind = 0
        lenIt = len(it)
        for i in range(lenIt):
            rct = it[-(i+1)].rect()
            if self.pointInRect(mPos, rct):
                ind = i
                break
        self.ui.slide1.setValue(ind+1)
        
        
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
        if len(self.exp)<=dove-1 or dove-1<0:
            return None
        else:
            self.ui.labelNumber.setText(str(dove))
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
        for p in self.exp[dove][0:]:
            if not self.ui.derivCkBox.isChecked():
                f = p.f
                z = p.z
            else:
                #sf = smartSgf(p.f,4,sgfDeg)
                if self.ui.jumpCkBox.isChecked():
                    peakThrPc = self.ui.peakThrsNumDbl.value()
                    derP,_ = pieceWiseSavGol(p.f,peakThrPc,sgfWinPcF,sgfDeg,0,pieces = True)
                    f = np.array([])
                    for d in derP:
                        f = np.concatenate((f,np.gradient(d)))
                    z = p.z
                else:
                    f,start,end = polishedDerive(p.f,sgfWinPcF,sgfWinPcG,sgfDeg,cutMe)
                    f = f[start:end]
                    z = p.z[start:end]
            if p == self.exp[dove][-1]:
                self.ui.grafo.plot(z,f,pen='b')
            else:
                self.ui.grafo.plot(z,f)
        if self.fitFlag:
            self.plotFit(-1)
        self.checkCurve(dove)
        if len(self.cursors)>=1:
            self.refreshCursors()
        if autorange:
            self.ui.grafo.autoRange()
    
    
    def checkCurve(self,dove):

        if self.lastOperation == 'peaks detection':
            self.populatePeaksCmb()
        
        if self.alignFlags[dove]:
            self.ui.grafo.plotItem.addLine(x=0)
            self.ui.grafo.plotItem.addLine(y=0)
            if self.peaksOnPlot:
                self.showPeaks()
            
    
    def batchConv(self):
        
        dirIn = str(QFileDialog.getExistingDirectory(self, 'Select a directory', './'))
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
                
    
    def showFit(self):
        
        self.plotFit(-1)
        self.ui.autoFitBtn.setEnabled(False)
        self.ui.rejectBtn.setEnabled(True)
       
    
    def findPeaks(self):
        try:
            if self.lastOperation != 'peaks detection':
                self.ui.rsqLimNumDbl.valueChanged.connect(self.findPeaks)
                self.ui.peakThrsNumDbl.valueChanged.connect(self.findPeaks)
                self.ui.peakLenPcNumDbl.valueChanged.connect(self.findPeaks)
            self.lastOperation = 'peaks detection'
            peakThrPc = self.ui.peakThrsNumDbl.value()
            distPcT = self.ui.peakLenPcNumDbl.value()
            rsqLim = self.ui.rsqLimNumDbl.value()
        
            i = 0
            for c in self.exp:
                if self.ui.jumpCkBox.isChecked():
                    res = c.getMarkedPeaks(-1,pwSgfPeaksFinder, peakModel = 2, argsPF = [peakThrPc,sgfWinPcG,sgfDeg,distPcT,True])
                else:
                    res = c.getMarkedPeaks(-1,peakFinder, peakModel = 2, argsPF = [sgfWinPcF,sgfWinPcG,sgfDeg,cutMe,peakThrPc,distPcT,True,rsqLim])
                if res<1:
                    c.relevant = False
                    self.bad.append(i)
                    self.badFlags[i] = True
                else:
                    c.relevant = True
                    try:
                        del self.bad[i]
                    except:
                        pass
                    self.badFlags[i] = False
                i+=1
                
            self.populatePeaksCmb()
            
            self.setStatus(4)
            
            self.refillList(self.ui.slide1.value())
        except Exception as e:
            print(e.message)
    
        
    def showHidePeaks(self):
        try:
            if self.ui.showPeakBtn.text() == 'Show Peaks':
                self.peaksOnPlot = True
                self.ui.showPeakBtn.setText('Hide Peaks')
                self.showPeaks()
                
            else:
                self.ui.showPeakBtn.setText('Show Peaks')
                self.peaksOnPlot = False
                self.goToCurve(self.ui.slide1.value())
                
        except Exception as e:
            print(e.message)
    
    
    def populatePeaksCmb(self):
        self.ui.peaksCmbBox.clear()
        self.ui.peaksCmbBox.addItem('Select a Peak')
        
        i = 0    
        for pk in self.exp[self.ui.slide1.value()-1][-1].peaks:
            self.ui.peaksCmbBox.addItem(str(i))
            i+=1
        self.ui.peaksCmbBox.setCurrentIndex(int(i>0))
        self.ui.peaksNum.setValue(len(self.exp[self.ui.slide1.value()-1][-1].peaks))
            
    
    def showPeaks(self):
        try:
            setData = False
            curveInd = len(self.exp[self.ui.slide1.value()-1])-1
            peakThrPc = self.ui.peakThrsNumDbl.value()
            distPcT = self.ui.peakLenPcNumDbl.value()
            rsqLim = self.ui.rsqLimNumDbl.value()
            if self.ui.jumpCkBox.isChecked():
                derP,_ = pieceWiseSavGol(self.exp[self.ui.slide1.value()-1][-1].f,peakThrPc,sgfWinPcF,sgfDeg,0,pieces = True)
                der = np.array([])
                for d in derP:
                    der = np.concatenate((der,np.gradient(d)))
            else:
                der,start,end = polishedDerive(self.exp[self.ui.slide1.value()-1][-1].f, sgfWinPcF, sgfWinPcG, sgfDeg, False)
            
            if self.exp[self.ui.slide1.value()-1][-1].peaks == []:
                return None
            res = len(self.exp[self.ui.slide1.value()-1][-1].peaks)
            peaksA = np.array([])
            zpeaksA = np.array([])
            derivpeaksA = np.array([])
            
            for pk in self.exp[self.ui.slide1.value()-1][-1].peaks:
                peaksA = np.concatenate((peaksA,pk.f))
                zpeaksA = np.concatenate((zpeaksA,pk.z))
                start = list(self.exp[self.ui.slide1.value()-1][-1].z).index(pk.z[0])
                end = list(self.exp[self.ui.slide1.value()-1][-1].z).index(pk.z[-1])
                derivpeaksA = np.concatenate((derivpeaksA,der[start:end+1]))
            self.populatePeaksCmb()
                
            self.ui.grafo.plot(zpeaksA,derivpeaksA if self.ui.derivCkBox.isChecked() else peaksA,pen = None,symbolPen='r',symbolBrush='r',symbol='o',symbolSize = 5)
        
        except Exception as e:
            print(e.message)
                
            
    def calcArea(self):
        
        ind = self.sender().currentIndex()-1
        if ind < 0:
            return None
        self.ui.peakDataTxt.clear()
        info = self.exp[self.ui.slide1.value()-1][-1].peaks[ind].getInfo()
        self.ui.peakDataTxt.insertPlainText(info)
    
    
    def savePeaks(self):
        
        if self.sender() == self.ui.saveWholePeakBtn:
            dirname = str(QFileDialog.getExistingDirectory(self, 'Select a directory for the peaks', './'))
            if dirname != '':
                for c in self.exp:
                    if len(c[-1].peaks)>0:
                        c[-1].peaks.saveCollection(dirname,(splitext(c.basename)[0]+'_peak'))
            else:
                return None
        
        else:
            peakThrPc = self.ui.peakThrsNumDbl.value()
            distPcT = self.ui.peakLenPcNumDbl.value()
            rsqLim = self.ui.rsqLimNumDbl.value()
        
            for c in self.exp:
                if len(c[-1].peaks) < 1:
                    c[-1].getPeaks(peakFinder, peakModel = 2, argsPF = [sgfWinPcF,sgfWinPcG,sgfDeg,cutMe,peakThrPc,distPcT,True,rsqLim])
        
            single = self.sender() == self.ui.savePeaksBtn
        
            table = self.exp.getPeaksStatsTable(single,True)
        
            header = 'Curve\tStart [nm]\tEnd [nm]\tApex z [nm]\tApex force [pN]\tBaseline [pN]\tArea [zJ]\n' if single else 'Curve\tMean Area [zJ]\tArea var [zJ]\tMean Height [zJ]\tHeight var [zJ]\tMean Length [zJ]\tLength var [zJ]\n'
        
            table = header+table
        
            filename = QFileDialog.getSaveFileName(self,'Choose the path for peaks stats')
        
            f = open(filename,'w')
            f.write(table)
    
    
    def rejectAlign(self):
        
        self.fitFlag = False
        self.goToCurve(self.ui.slide1.value())
        for i in range(len(self.exp)):
            self.ctPoints[i] = None
        
    
    def plotFit(self,segInd):
        try:
            c = self.exp[self.ui.slide1.value()-1]
            fits, ctPt,_,_ = fitCnNC(c[segInd],'>',sgfWinPc,sgfDeg,compWinPc, thPc = self.ui.slopePcNum.value())
            if self.ctPoints[self.ui.slide1.value()-1] == None:
                self.ctPoints[self.ui.slide1.value()-1] = ctPt
            fit = np.concatenate((fits[0],fits[1]))
            self.ui.grafo.plot(c[segInd].z,fit,pen='r')
            self.fitFlag = True
        except Exception as e:
            print(e.message)


    def recalcSensitivity(self):
        try:
            for c in self.exp:
                print('Sensitivity before: {0}'.format(c.sensitivity))
                print('K: {0}'.format(c.k))
                _,_,_,fits = fitCnNC(c[-1],'>',sgfWinPc,sgfDeg,compWinPc, thPc = self.ui.slopePcNum.value())
                print('Linear Fit: {0}'.format(fits[0]))
                c.changeSens(c.k*c.sensitivity/fits[0][0])
                print('Sensitivity after: {0}'.format(c.sensitivity))
        except:
            pass

    
    def align(self):
        culprit = self.sender()
        self.fitFlag = False
        self.lastOperation = 'alignement'
        if culprit is self.ui.alignBtn:
            try:
                logString = 'Aligning {0}\n'.format(self.exp[self.ui.slide1.value()-1].basename)
                self.simpleLogger(logString)
                fits,contactPt, valid,_= fitCnNC(self.exp[self.ui.slide1.value()-1][-1],'>',sgfWinPc,sgfDeg,compWinPc,thPc = self.ui.slopePcNum.value())
                if self.ctPoints[self.ui.slide1.value()-1] != None:
                    contactPt = self.ctPoints[self.ui.slide1.value()-1]
                    self.ctPoints[self.ui.slide1.value()-1] = None
                    
                for s in self.exp[self.ui.slide1.value()-1][1:]:
                    s.f = s.f[np.where(s.z>=contactPt[0])]-np.mean(fits[1])#contactPt[1]
                    s.z = s.z[np.where(s.z>=contactPt[0])]-contactPt[0]
                self.exp[self.ui.slide1.value()-1].relevant = valid
                if not valid:
                    self.bad.append(self.ui.slide1.value()-1)
                    self.bad.sort()
                    self.badFlags[self.ui.slide1.value()-1] = False
                self.alignFlags[self.ui.slide1.value()-1] = True
                del self.exp[self.ui.slide1.value()-1][0]
                self.goToCurve(self.ui.slide1.value())
                self.ui.slide1.setValue(self.ui.slide1.value())
                self.ui.slide2.setValue(self.ui.slide1.value())
            except Exception as e:
                print(e.message)
        else:
            pmax = len(self.exp)
            logString = 'Aligning all curves...\n'
            self.simpleLogger(logString)
            progress = QProgressDialog("Aligning curves...", "Cancel aligning", 0, pmax);
            i=0
            for c in self.exp:
                print(c.basename)
                progress.setValue(i)
                if (progress.wasCanceled()):
                    break
                if self.alignFlags[i]:
                    i=i+1
                    continue
                try:
                    fits,contactPt,valid,_ = fitCnNC(c[-1],'>',sgfWinPc,sgfDeg,compWinPc,thPc = self.ui.slopePcNum.value())
                    if self.ctPoints[i] != None:
                        contactPt = self.ctPoints[i]
                        self.ctPoints[i] = None
                    c.relevant = valid
                    if not valid:
                        self.bad.append(i)
                        self.bad.sort()
                        self.badFlags[i] = False
                        
                    for s in c[1:]:
                        s.f = s.f[np.where(s.z>=contactPt[0])]-np.mean(fits[1])#contactPt[1]
                        s.z = s.z[np.where(s.z>=contactPt[0])]-contactPt[0]
                except Exception as e:
                    print(e.message)
                self.alignFlags[i] = True
                del c[0]
                i=i+1
            progress.setValue(pmax)
            logString = 'Curves aligned\n'
            self.simpleLogger(logString)
            self.goToCurve(1)
            self.ui.slide1.setValue(0)
            self.setStatus(3)
        if len(self.cursors)>=1:
            self.refreshCursors()
        self.refillList()


    def reload(self):
        pmax = len(self.exp)
        self.bad = []
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        logString = 'Reloading all the curves\n'
        self.simpleLogger(logString)
        progress = QProgressDialog("Reloading curves...", "Cancel reloading", 0, pmax);
        i=0
        tempExp = deepcopy(self.exp)
        self.exp = None
        self.exp = experiment.experiment()
        for c in tempExp:
            aligned = c[0].direction == 'far'
            self.alignFlags.append(aligned)
            self.badFlags.append(True)
            self.ctPoints [i] = None
            i+=1
            progress.setValue(i)
            self.exp.addFiles([c.filename])
        progress.setValue(pmax)
        QApplication.restoreOverrideCursor()
        tempExp = None
        self.fitFlag = False
        self.setStatus(2)
        if np.array(self.alignFlags).all():
            self.setStatus(3)
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
            if self.globDir == '':
                dir = join(split(c.filename)[0],'aligned')
            else:
                dir = self.globDir

            if not exists(dir):
                makedirs(dir)
            onlyFile,ext = splitext(c.basename)
            if cc[0].direction == 'near':
                del cc[0]
            basename = onlyFile+'_aligned'+ext
            filename = join(dir,basename)
            if exists(filename):
                filename = str(QFileDialog.getSaveFileName(self,'The name you chose already exists. Select another one or pick the same to overwrite',filename))
            logString = 'Saving {0} aligned version in {1}\n'.format(split(filename)[1],split(filename)[0])
            self.simpleLogger(logString)
            cc.save(filename)
            cc = None
        else:
            for i in range(len(self.exp)):
                c = self.exp[i]
                if not self.alignFlags[i] or len(c)<1:
                    continue
                cc = deepcopy(c)
                if self.globDir == '':     
                    dir = join(split(c.filename)[0],'aligned')
                else:
                    dir = self.globDir
                if not exists(dir):
                    makedirs(dir)
                onlyFile,ext = splitext(c.basename)
                if cc[0].direction == 'near':
                    del cc[0]
                basename = onlyFile+'_aligned'+ext
                filename = join(dir,basename)
                if exists(filename):
                    filename = str(QFileDialog.getSaveFileName(self,'The name you chose already exists. Select another one or pick the same to overwrite',filename))
                logString = 'Saving {0} aligned version in {1}\n'.format(split(filename)[1],split(filename)[0])
                self.simpleLogger(logString)
                cc.save(filename)
                cc = None
        

    def simpleLogger(self,entry):
        completeEntry = strftime('%Y/%m/%d') + '-' + strftime('%H:%M:%S') + ' -- ' + entry
        self.ui.logTxt.insertPlainText(completeEntry)
        
    
    def logOperations(self,operation,total,removed):
        logString = 'Preformed: \"{0}\". Removed {1} curves of {2}'.format(self.lastOperation,removed,total)+'\n'
        self.simpleLogger(logString)
    
        
    def removeCurve(self):
        culprit = self.sender()
        warningDial = QMessageBox(self)
        warningDial.setWindowTitle(culprit.text())
        warningDial.setText('Do you want to procede?')
        warningDial.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        warningDial.setDefaultButton(QMessageBox.No)
        answer = warningDial.exec_()
        if answer == 65536:
            return None
        if culprit is self.ui.removeBtn:
            ind = self.ui.slide1.value()-1
            logString = '{0} Removed\n'.format(self.exp[ind].basename)
            self.simpleLogger(logString)
            del self.exp[ind]
            del self.alignFlags[ind]
            del self.badFlags[ind]
            del self.ctPoints[ind]
            try:
                badInd = self.bad.index(ind)
                for i in range(len(self.bad[badInd+1])):
                    self.bad[i] -= 1
                del self.bad[badInd]
            except:
                pass
            
            if len(self.exp)<1:
                self.setStatus(1)
                self.ui.grafo.clear()
            else:
                self.goToCurve(1)
        else:
            totalNum = len(self.exp)
            tempExp = [k for j, k in enumerate(self.exp) if j in self.bad]
            for t in tempExp:
                logString = '{0} Removed\n'.format(t.basename)
                self.simpleLogger(logString)
                del self.exp[t.basename]
            self.alignFlags = [k for j, k in enumerate(self.alignFlags) if j not in self.bad]
            self.ctPoints = [k for j, k in enumerate(self.ctPoints) if j not in self.bad]
            self.badFlags = [k for j, k in enumerate(self.badFlags) if j not in self.bad]
            self.logOperations(self.lastOperation, totalNum, len(tempExp))
            self.bad = []
            self.ui.removeBOBtn.setEnabled(False)
            if len(self.exp)<1:
                self.setStatus(1)
                self.ui.grafo.clear()
            else:
                self.ui.slide1.setValue(1)
                
        
        self.refillList()
        
    
    def overlay(self):
        alpha = 256.0/(len(self.exp)-len(self.bad))
        color = pg.mkColor(0,0,0,alpha)
        self.ui.grafo.clear()
        for i in range(len(self.exp)):
            if self.alignFlags[i] and self.exp[i].relevant:
                self.ui.grafo.plot(self.exp[i][-1].z,self.exp[i][-1].f,pen=None,symbol='o',symbolSize = 2,symbolPen = color, symbolBrush = color)
                
                
    def changeStatus(self):
        
        print(self.bad)
        
        ind = self.ui.slide1.value()-1
        if self.alignFlags[ind]:
            self.exp[ind].relevant = not self.exp[ind].relevant
            if not self.badFlags[ind]:
                badInd = self.bad.index(ind)
                del self.bad[badInd]
            else:
                self.bad.append(ind)
                self.ui.removeBOBtn.setEnabled(True)
            self.bad.sort()
            self.badFlags[ind] = not self.badFlags[ind]
            self.refillList()
    
    
    def closeExp(self):
        
        self.ui.grafo.clear()
        self.exp = []
        self.fitFlag = False
        self.alignFlags = []
        self.ctPoints = []
        self.bad = []
        self.badFlags = []
        self.exp = experiment.experiment()
        self.refillList()
        logString = 'Experiment closed\n'
        self.simpleLogger(logString)
        self.globDir = ''
        self.ui.setPathBtn.setStyleSheet('background-color: none')
        self.cursors = []
        for i in range(self.ui.cursCmbBox.count()):
            self.ui.cursCmbBox.removeItem(i)
            self.ui.cursCmpCmbBox.removeItem(i+1)
        self.ui.currCursXvalNumDbl.setValue(0.0)
        self.ui.currCursYvalNumDbl.setValue(0.0)
        self.ui.currCursXdelNumDbl.setValue(0.0)
        self.ui.currCursYdelNumDbl.setValue(0.0)
        self.setStatus(1)
        
    
    def setSavePath(self):
        
        dirname = str(QFileDialog.getExistingDirectory(self, 'Select a directory', './'))
        if dirname != '':
            logString = 'Global save path set at: {0}'.format(dirname)
            self.simpleLogger(logString)
            self.globDir = dirname
            self.ui.setPathBtn.setStyleSheet('background-color: red')
    
    
    def checked(self):
        self.goToCurve(self.ui.slide1.value())    
    
    
    def show2Dhist(self):
        goodF = []
        goodZ = []
        shortestSize = float('Inf')
        for c in self.exp:
            if c.relevant:
                shortestSize = min(c[-1].f.shape[0],shortestSize) 
                goodF.append(c[-1].f)
                goodZ.append(c[-1].z)
        
        emptyF = np.array([])
        emptyZ = np.array([])
        
        for i in range(len(goodF)):
            emptyF = np.concatenate((emptyF,goodF[i][:shortestSize]))
            emptyZ = np.concatenate((emptyZ,goodZ[i][:shortestSize]))
        
        histo = np.histogram2d(emptyZ, emptyF, [shortestSize,len(goodF)])
        hist = histo[0]
        hist = ((hist - np.min(hist))/(np.max(hist)-np.min(hist))*255).astype(np.uint8)
        img = Image.fromarray(hist)
        pix = QPixmap(img.convert('RGBA').tostring('raw','RGBA'))
        pixG = QGraphicsPixmapItem(pix)
        self.ui.grafo.clear()
        self.ui.grafo.addItem(pixG)
        self.ui.grafo.update()
        
        
    def addCursor(self):
        
        curveInd = len(self.exp[self.ui.slide1.value()-1])-1
        lim = len(self.cursors)
        currInd = lim
        for i in range(lim):
            currName = self.cursColors[i][0]
            names = []
            for c in range(self.ui.cursCmbBox.count()):
                names.append(self.ui.cursCmbBox.itemText(c))
            if currName not in names:
                currInd = i
                break
        self.cursors.append(cursor(self.ui.grafo.plotItem,curveInd,True,True,'+',self.cursColors[currInd][1]))
        self.ui.cursCmbBox.addItem(self.cursColors[currInd][0])
        self.ui.cursCmpCmbBox.addItem(self.cursColors[currInd][0])
        
        self.ui.cursCmbBox.setCurrentIndex(currInd)
        QObject.connect(self.cursors[self.ui.cursCmbBox.currentIndex()], SIGNAL(_fromUtf8("moved()")), self.updateCursNums)
        if len(self.cursors) == 4:
            self.ui.addCursBtn.setEnabled(False)
        if not self.ui.removeCursBtn.isEnabled():
            self.ui.removeCursBtn.setEnabled(True)
            
        
    def updateCursNums(self):
        
        position = self.sender().pos()
        self.ui.cursCmbBox.setCurrentIndex(self.cursors.index(self.sender()))
        self.ui.currCursXvalNumDbl.setValue(position[0])
        self.ui.currCursYvalNumDbl.setValue(position[1])
        if self.ui.cursCmpCmbBox.currentIndex() != 0 :
            compCur = self.cursors[self.ui.cursCmpCmbBox.currentIndex()-1].pos()
            self.ui.currCursXdelNumDbl.setValue(position[0]-compCur[0])
            self.ui.currCursYdelNumDbl.setValue(position[1]-compCur[1])
    
    
    def removeCursor(self):
        if not self.ui.addCursBtn.isEnabled():
            self.ui.addCursBtn.setEnabled(True)
        ind = len(self.cursors)-1#self.ui.cursCmbBox.currentIndex()
        self.cursors[ind].suicide()
        self.ui.grafo.update()
        del self.cursors[ind]
        self.ui.cursCmbBox.removeItem(ind)
        self.ui.cursCmpCmbBox.removeItem(ind+1)
        if len(self.cursors) == 0:
            self.ui.removeCursBtn.setEnabled(False)    
    
    
    def refreshCursors(self):
        
        lim = len(self.cursors)
        self.cursors = []
        
        res = len(self.exp[self.ui.slide1.value()-1][-1].peaks)

        for i in range(lim):
            curveInd = len(self.exp[self.ui.slide1.value()-1])-1
            currName = self.ui.cursCmbBox.itemText(i)
            for k in self.cursColors.keys():
                if currName in self.cursColors[k]:
                    currInd = i
            self.cursors.append(cursor(self.ui.grafo.plotItem,curveInd,True,True,'+',self.cursColors[currInd][1]))
            QObject.connect(self.cursors[-1], SIGNAL(_fromUtf8("moved()")), self.updateCursNums)
        
    
    def setConnections(self):

        self.ui.slide1.valueChanged.connect(self.ui.slide2.setValue)
        self.ui.slide2.valueChanged.connect(self.ui.slide1.setValue)
        self.ui.slide2.valueChanged.connect(self.ui.curveNameCmbBox.setCurrentIndex)
        self.ui.slide1.valueChanged.connect(self.ui.curveNameCmbBox.setCurrentIndex)
        self.ui.curveNameCmbBox.currentIndexChanged.connect(self.ui.slide1.setValue)
        self.ui.curveNameCmbBox.currentIndexChanged.connect(self.ui.slide2.setValue)
        self.ui.slide1.valueChanged.connect(self.goToCurve)

        self.ui.bAddDir.clicked.connect(self.addDirectory)
        self.ui.bAddFiles.clicked.connect(self.addFiles)

        self.ui.convr9Btn.clicked.connect(self.batchConv)

        self.ui.updateKBtn.clicked.connect(self.updateK)
        self.ui.updateAllKBtn.clicked.connect(self.updateK)
        self.ui.updateNmVBtn.clicked.connect(self.updateSens)
        self.ui.updateAllNmVBtn.clicked.connect(self.updateSens)
        self.ui.updateSpeedBtn.clicked.connect(self.updateSpeed)
        self.ui.updateAllSpeedBtn.clicked.connect(self.updateSpeed)
        self.ui.hist2dBtn.clicked.connect(self.show2Dhist)

        self.ui.autoFitBtn.clicked.connect(self.showFit)
        self.ui.rejectBtn.clicked.connect(self.rejectAlign)
        self.ui.alignBtn.clicked.connect(self.align)
        self.ui.alignAllBtn.clicked.connect(self.align)
        self.ui.reloadBtn.clicked.connect(self.reload)
        self.ui.saveBtn.clicked.connect(self.saveAligned)
        self.ui.saveAllBtn.clicked.connect(self.saveAligned)
        self.ui.removeBtn.clicked.connect(self.removeCurve)
        self.ui.removeBOBtn.clicked.connect(self.removeCurve)
        self.ui.showPeakBtn.clicked.connect(self.showHidePeaks)
        self.ui.findPeaksBtn.clicked.connect(self.findPeaks)
        self.ui.savePeaksBtn.clicked.connect(self.savePeaks)
        self.ui.savePeaksStatsBtn.clicked.connect(self.savePeaks)
        self.ui.saveWholePeakBtn.clicked.connect(self.savePeaks)

        self.ui.overlayBtn.clicked.connect(self.overlay)
        self.ui.chgStatBtn.clicked.connect(self.changeStatus)
        self.ui.closeExpBtn.clicked.connect(self.closeExp)
        self.ui.setPathBtn.clicked.connect(self.setSavePath)
        self.ui.addCursBtn.clicked.connect(self.addCursor)
        self.ui.removeCursBtn.clicked.connect(self.removeCursor)
        
        self.ui.peaksCmbBox.currentIndexChanged.connect(self.calcArea)
        self.ui.derivCkBox.clicked.connect(self.checked)

        self.ui.recalcSensBtn.clicked.connect(self.recalcSensitivity)
        
        #QMetaObject.connectSlotsByName(self)


if __name__ == "__main__":

    print('Not for standalone use')