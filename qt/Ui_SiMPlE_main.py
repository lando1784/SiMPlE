# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ettore/GIT/SiMPlE/qt/SiMPlE_main.ui'
#
# Created: Tue Jul 28 19:43:26 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_facewindow(object):
    def setupUi(self, facewindow):
        facewindow.setObjectName(_fromUtf8("facewindow"))
        facewindow.resize(1064, 850)
        self.simpleCtWidget = QtGui.QWidget(facewindow)
        self.simpleCtWidget.setObjectName(_fromUtf8("simpleCtWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.simpleCtWidget)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.grafo = PlotWidget(self.simpleCtWidget)
        self.grafo.setObjectName(_fromUtf8("grafo"))
        self.horizontalLayout.addWidget(self.grafo)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.griglia = QtGui.QGraphicsView(self.simpleCtWidget)
        self.griglia.setObjectName(_fromUtf8("griglia"))
        self.verticalLayout_2.addWidget(self.griglia)
        self.slide2 = QtGui.QDial(self.simpleCtWidget)
        self.slide2.setObjectName(_fromUtf8("slide2"))
        self.verticalLayout_2.addWidget(self.slide2)
        self.slide1 = QtGui.QScrollBar(self.simpleCtWidget)
        self.slide1.setOrientation(QtCore.Qt.Horizontal)
        self.slide1.setObjectName(_fromUtf8("slide1"))
        self.verticalLayout_2.addWidget(self.slide1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.setStretch(0, 6)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.functionsTabs = QtGui.QTabWidget(self.simpleCtWidget)
        self.functionsTabs.setObjectName(_fromUtf8("functionsTabs"))
        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName(_fromUtf8("tab_5"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.tab_5)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.loadBox = QtGui.QGroupBox(self.tab_5)
        self.loadBox.setObjectName(_fromUtf8("loadBox"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.loadBox)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.bAddDir = QtGui.QPushButton(self.loadBox)
        self.bAddDir.setObjectName(_fromUtf8("bAddDir"))
        self.verticalLayout.addWidget(self.bAddDir)
        self.bAddFiles = QtGui.QPushButton(self.loadBox)
        self.bAddFiles.setObjectName(_fromUtf8("bAddFiles"))
        self.verticalLayout.addWidget(self.bAddFiles)
        self.convr9Btn = QtGui.QPushButton(self.loadBox)
        self.convr9Btn.setObjectName(_fromUtf8("convr9Btn"))
        self.verticalLayout.addWidget(self.convr9Btn)
        self.reloadBtn = QtGui.QPushButton(self.loadBox)
        self.reloadBtn.setEnabled(False)
        self.reloadBtn.setObjectName(_fromUtf8("reloadBtn"))
        self.verticalLayout.addWidget(self.reloadBtn)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.horizontalLayout_4.setStretch(0, 2)
        self.horizontalLayout_2.addWidget(self.loadBox)
        self.saveBox = QtGui.QGroupBox(self.tab_5)
        self.saveBox.setObjectName(_fromUtf8("saveBox"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.saveBox)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.setPathBtn = QtGui.QPushButton(self.saveBox)
        self.setPathBtn.setEnabled(False)
        self.setPathBtn.setObjectName(_fromUtf8("setPathBtn"))
        self.verticalLayout_4.addWidget(self.setPathBtn)
        self.saveBtn = QtGui.QPushButton(self.saveBox)
        self.saveBtn.setEnabled(False)
        self.saveBtn.setObjectName(_fromUtf8("saveBtn"))
        self.verticalLayout_4.addWidget(self.saveBtn)
        self.saveAllBtn = QtGui.QPushButton(self.saveBox)
        self.saveAllBtn.setEnabled(False)
        self.saveAllBtn.setObjectName(_fromUtf8("saveAllBtn"))
        self.verticalLayout_4.addWidget(self.saveAllBtn)
        self.horizontalLayout_2.addWidget(self.saveBox)
        self.removeBox = QtGui.QGroupBox(self.tab_5)
        self.removeBox.setObjectName(_fromUtf8("removeBox"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.removeBox)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.chgStatBtn = QtGui.QPushButton(self.removeBox)
        self.chgStatBtn.setEnabled(False)
        self.chgStatBtn.setObjectName(_fromUtf8("chgStatBtn"))
        self.verticalLayout_5.addWidget(self.chgStatBtn)
        self.removeBtn = QtGui.QPushButton(self.removeBox)
        self.removeBtn.setEnabled(False)
        self.removeBtn.setObjectName(_fromUtf8("removeBtn"))
        self.verticalLayout_5.addWidget(self.removeBtn)
        self.removeBOBtn = QtGui.QPushButton(self.removeBox)
        self.removeBOBtn.setEnabled(False)
        self.removeBOBtn.setObjectName(_fromUtf8("removeBOBtn"))
        self.verticalLayout_5.addWidget(self.removeBOBtn)
        self.closeExpBtn = QtGui.QPushButton(self.removeBox)
        self.closeExpBtn.setEnabled(False)
        self.closeExpBtn.setObjectName(_fromUtf8("closeExpBtn"))
        self.verticalLayout_5.addWidget(self.closeExpBtn)
        self.horizontalLayout_2.addWidget(self.removeBox)
        self.horizontalLayout_2.setStretch(0, 4)
        self.horizontalLayout_2.setStretch(1, 4)
        self.horizontalLayout_2.setStretch(2, 4)
        self.functionsTabs.addTab(self.tab_5, _fromUtf8(""))
        self.tab_6 = QtGui.QWidget()
        self.tab_6.setObjectName(_fromUtf8("tab_6"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.tab_6)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.fromFileBox = QtGui.QGroupBox(self.tab_6)
        self.fromFileBox.setObjectName(_fromUtf8("fromFileBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.fromFileBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_4 = QtGui.QLabel(self.fromFileBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.kNumDbl = QtGui.QDoubleSpinBox(self.fromFileBox)
        self.kNumDbl.setEnabled(False)
        self.kNumDbl.setMaximum(1000.0)
        self.kNumDbl.setObjectName(_fromUtf8("kNumDbl"))
        self.gridLayout_2.addWidget(self.kNumDbl, 0, 1, 1, 1)
        self.updateKBtn = QtGui.QPushButton(self.fromFileBox)
        self.updateKBtn.setEnabled(False)
        self.updateKBtn.setObjectName(_fromUtf8("updateKBtn"))
        self.gridLayout_2.addWidget(self.updateKBtn, 0, 2, 1, 1)
        self.updateAllKBtn = QtGui.QPushButton(self.fromFileBox)
        self.updateAllKBtn.setEnabled(False)
        self.updateAllKBtn.setObjectName(_fromUtf8("updateAllKBtn"))
        self.gridLayout_2.addWidget(self.updateAllKBtn, 0, 3, 1, 1)
        self.label_5 = QtGui.QLabel(self.fromFileBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.nmVNumDbl = QtGui.QDoubleSpinBox(self.fromFileBox)
        self.nmVNumDbl.setEnabled(False)
        self.nmVNumDbl.setMaximum(1000.0)
        self.nmVNumDbl.setObjectName(_fromUtf8("nmVNumDbl"))
        self.gridLayout_2.addWidget(self.nmVNumDbl, 1, 1, 1, 1)
        self.updateNmVBtn = QtGui.QPushButton(self.fromFileBox)
        self.updateNmVBtn.setEnabled(False)
        self.updateNmVBtn.setObjectName(_fromUtf8("updateNmVBtn"))
        self.gridLayout_2.addWidget(self.updateNmVBtn, 1, 2, 1, 1)
        self.updateAllNmVBtn = QtGui.QPushButton(self.fromFileBox)
        self.updateAllNmVBtn.setEnabled(False)
        self.updateAllNmVBtn.setObjectName(_fromUtf8("updateAllNmVBtn"))
        self.gridLayout_2.addWidget(self.updateAllNmVBtn, 1, 3, 1, 1)
        self.label_6 = QtGui.QLabel(self.fromFileBox)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        self.speedNumDbl = QtGui.QDoubleSpinBox(self.fromFileBox)
        self.speedNumDbl.setEnabled(False)
        self.speedNumDbl.setMaximum(1000.0)
        self.speedNumDbl.setObjectName(_fromUtf8("speedNumDbl"))
        self.gridLayout_2.addWidget(self.speedNumDbl, 2, 1, 1, 1)
        self.updateSpeedBtn = QtGui.QPushButton(self.fromFileBox)
        self.updateSpeedBtn.setEnabled(False)
        self.updateSpeedBtn.setObjectName(_fromUtf8("updateSpeedBtn"))
        self.gridLayout_2.addWidget(self.updateSpeedBtn, 2, 2, 1, 1)
        self.updateAllSpeedBtn = QtGui.QPushButton(self.fromFileBox)
        self.updateAllSpeedBtn.setEnabled(False)
        self.updateAllSpeedBtn.setObjectName(_fromUtf8("updateAllSpeedBtn"))
        self.gridLayout_2.addWidget(self.updateAllSpeedBtn, 2, 3, 1, 1)
        self.horizontalLayout_5.addWidget(self.fromFileBox)
        self.fitNpeakBox = QtGui.QGroupBox(self.tab_6)
        self.fitNpeakBox.setObjectName(_fromUtf8("fitNpeakBox"))
        self.formLayout = QtGui.QFormLayout(self.fitNpeakBox)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_7 = QtGui.QLabel(self.fitNpeakBox)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_7)
        self.slopePcNum = QtGui.QSpinBox(self.fitNpeakBox)
        self.slopePcNum.setEnabled(False)
        self.slopePcNum.setMinimum(1)
        self.slopePcNum.setMaximum(100)
        self.slopePcNum.setProperty("value", 15)
        self.slopePcNum.setObjectName(_fromUtf8("slopePcNum"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.slopePcNum)
        self.movVarPcNum = QtGui.QSpinBox(self.fitNpeakBox)
        self.movVarPcNum.setEnabled(False)
        self.movVarPcNum.setMinimum(1)
        self.movVarPcNum.setMaximum(100)
        self.movVarPcNum.setProperty("value", 10)
        self.movVarPcNum.setObjectName(_fromUtf8("movVarPcNum"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.movVarPcNum)
        self.peakThrsPcNum = QtGui.QSpinBox(self.fitNpeakBox)
        self.peakThrsPcNum.setEnabled(False)
        self.peakThrsPcNum.setMinimum(1)
        self.peakThrsPcNum.setMaximum(100)
        self.peakThrsPcNum.setProperty("value", 70)
        self.peakThrsPcNum.setObjectName(_fromUtf8("peakThrsPcNum"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.peakThrsPcNum)
        self.label_8 = QtGui.QLabel(self.fitNpeakBox)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_8)
        self.label_9 = QtGui.QLabel(self.fitNpeakBox)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_9)
        self.label_10 = QtGui.QLabel(self.fitNpeakBox)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_10)
        self.movAvgPcNum = QtGui.QSpinBox(self.fitNpeakBox)
        self.movAvgPcNum.setEnabled(False)
        self.movAvgPcNum.setMinimum(1)
        self.movAvgPcNum.setMaximum(100)
        self.movAvgPcNum.setProperty("value", 20)
        self.movAvgPcNum.setObjectName(_fromUtf8("movAvgPcNum"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.movAvgPcNum)
        self.horizontalLayout_5.addWidget(self.fitNpeakBox)
        self.functionsTabs.addTab(self.tab_6, _fromUtf8(""))
        self.tab_7 = QtGui.QWidget()
        self.tab_7.setObjectName(_fromUtf8("tab_7"))
        self.gridLayout = QtGui.QGridLayout(self.tab_7)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.autoFitBtn = QtGui.QPushButton(self.tab_7)
        self.autoFitBtn.setEnabled(False)
        self.autoFitBtn.setObjectName(_fromUtf8("autoFitBtn"))
        self.gridLayout.addWidget(self.autoFitBtn, 0, 0, 1, 1)
        self.rejectBtn = QtGui.QPushButton(self.tab_7)
        self.rejectBtn.setEnabled(False)
        self.rejectBtn.setObjectName(_fromUtf8("rejectBtn"))
        self.gridLayout.addWidget(self.rejectBtn, 0, 1, 1, 1)
        self.alignBtn = QtGui.QPushButton(self.tab_7)
        self.alignBtn.setEnabled(False)
        self.alignBtn.setObjectName(_fromUtf8("alignBtn"))
        self.gridLayout.addWidget(self.alignBtn, 2, 0, 1, 1)
        self.alignAllBtn = QtGui.QPushButton(self.tab_7)
        self.alignAllBtn.setEnabled(False)
        self.alignAllBtn.setObjectName(_fromUtf8("alignAllBtn"))
        self.gridLayout.addWidget(self.alignAllBtn, 3, 0, 1, 1)
        self.overlayBtn = QtGui.QPushButton(self.tab_7)
        self.overlayBtn.setEnabled(False)
        self.overlayBtn.setObjectName(_fromUtf8("overlayBtn"))
        self.gridLayout.addWidget(self.overlayBtn, 5, 0, 1, 1)
        self.showPeakBtn = QtGui.QPushButton(self.tab_7)
        self.showPeakBtn.setEnabled(False)
        self.showPeakBtn.setObjectName(_fromUtf8("showPeakBtn"))
        self.gridLayout.addWidget(self.showPeakBtn, 4, 0, 1, 1)
        self.removePeakBtn = QtGui.QPushButton(self.tab_7)
        self.removePeakBtn.setEnabled(False)
        self.removePeakBtn.setObjectName(_fromUtf8("removePeakBtn"))
        self.gridLayout.addWidget(self.removePeakBtn, 4, 1, 1, 1)
        self.functionsTabs.addTab(self.tab_7, _fromUtf8(""))
        self.horizontalLayout_3.addWidget(self.functionsTabs)
        self.logTxt = QtGui.QTextEdit(self.simpleCtWidget)
        self.logTxt.setObjectName(_fromUtf8("logTxt"))
        self.horizontalLayout_3.addWidget(self.logTxt)
        self.horizontalLayout_3.setStretch(0, 6)
        self.horizontalLayout_3.setStretch(1, 3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label = QtGui.QLabel(self.simpleCtWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_6.addWidget(self.label)
        self.label_2 = QtGui.QLabel(self.simpleCtWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_6.addWidget(self.label_2)
        self.labFilename = QtGui.QLabel(self.simpleCtWidget)
        self.labFilename.setObjectName(_fromUtf8("labFilename"))
        self.horizontalLayout_6.addWidget(self.labFilename)
        self.label_3 = QtGui.QLabel(self.simpleCtWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_6.addWidget(self.label_3)
        self.labelNumber = QtGui.QLabel(self.simpleCtWidget)
        self.labelNumber.setObjectName(_fromUtf8("labelNumber"))
        self.horizontalLayout_6.addWidget(self.labelNumber)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.horizontalLayout_6.setStretch(0, 2)
        self.horizontalLayout_6.setStretch(1, 2)
        self.horizontalLayout_6.setStretch(2, 5)
        self.horizontalLayout_6.setStretch(3, 2)
        self.horizontalLayout_6.setStretch(4, 2)
        self.horizontalLayout_6.setStretch(5, 15)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.verticalLayout_3.setStretch(0, 12)
        self.verticalLayout_3.setStretch(1, 4)
        self.verticalLayout_3.setStretch(2, 1)
        facewindow.setCentralWidget(self.simpleCtWidget)
        self.menubar = QtGui.QMenuBar(facewindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1064, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        facewindow.setMenuBar(self.menubar)

        self.retranslateUi(facewindow)
        self.functionsTabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(facewindow)

    def retranslateUi(self, facewindow):
        facewindow.setWindowTitle(_translate("facewindow", "MainWindow", None))
        self.loadBox.setTitle(_translate("facewindow", "Load", None))
        self.bAddDir.setText(_translate("facewindow", "Add DIR", None))
        self.bAddFiles.setText(_translate("facewindow", "Add Files", None))
        self.convr9Btn.setText(_translate("facewindow", "Convert R9 files", None))
        self.reloadBtn.setText(_translate("facewindow", "Reload", None))
        self.saveBox.setTitle(_translate("facewindow", "Save", None))
        self.setPathBtn.setText(_translate("facewindow", "Set Path", None))
        self.saveBtn.setText(_translate("facewindow", "Save", None))
        self.saveAllBtn.setText(_translate("facewindow", "Save All", None))
        self.removeBox.setTitle(_translate("facewindow", "Change and remove", None))
        self.chgStatBtn.setText(_translate("facewindow", "Change Status", None))
        self.removeBtn.setText(_translate("facewindow", "Remove Curve", None))
        self.removeBOBtn.setText(_translate("facewindow", "Remove bad ones", None))
        self.closeExpBtn.setText(_translate("facewindow", "Close Exp", None))
        self.functionsTabs.setTabText(self.functionsTabs.indexOf(self.tab_5), _translate("facewindow", "Files Management", None))
        self.fromFileBox.setTitle(_translate("facewindow", "From File", None))
        self.label_4.setText(_translate("facewindow", "k [N/nm]", None))
        self.updateKBtn.setText(_translate("facewindow", "UPDATE", None))
        self.updateAllKBtn.setText(_translate("facewindow", "UPDATE ALL", None))
        self.label_5.setText(_translate("facewindow", "Sensitivity [nm/V]", None))
        self.updateNmVBtn.setText(_translate("facewindow", "UPDATE", None))
        self.updateAllNmVBtn.setText(_translate("facewindow", "UPDATE ALL", None))
        self.label_6.setText(_translate("facewindow", "Speed [nm/s]", None))
        self.updateSpeedBtn.setText(_translate("facewindow", "UPDATE", None))
        self.updateAllSpeedBtn.setText(_translate("facewindow", "UPDATE ALL", None))
        self.fitNpeakBox.setTitle(_translate("facewindow", "Fitting and Peak finding", None))
        self.label_7.setText(_translate("facewindow", "Slope tolerance %", None))
        self.label_8.setText(_translate("facewindow", "Peak thrsh %", None))
        self.label_9.setText(_translate("facewindow", "Movig var win %", None))
        self.label_10.setText(_translate("facewindow", "Moving avg %", None))
        self.functionsTabs.setTabText(self.functionsTabs.indexOf(self.tab_6), _translate("facewindow", "Curve Params", None))
        self.autoFitBtn.setText(_translate("facewindow", "Show Fit", None))
        self.rejectBtn.setText(_translate("facewindow", "Remove Fit", None))
        self.alignBtn.setText(_translate("facewindow", "Align", None))
        self.alignAllBtn.setText(_translate("facewindow", "Align All", None))
        self.overlayBtn.setText(_translate("facewindow", "Overlay", None))
        self.showPeakBtn.setText(_translate("facewindow", "Show Peaks", None))
        self.removePeakBtn.setText(_translate("facewindow", "Remove Peaks", None))
        self.functionsTabs.setTabText(self.functionsTabs.indexOf(self.tab_7), _translate("facewindow", "Plot Options", None))
        self.label.setText(_translate("facewindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Current curve</span></p></body></html>", None))
        self.label_2.setText(_translate("facewindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Name: </span></p></body></html>", None))
        self.labFilename.setText(_translate("facewindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">//</span></p></body></html>", None))
        self.label_3.setText(_translate("facewindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Number: </span></p></body></html>", None))
        self.labelNumber.setText(_translate("facewindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">0</span></p></body></html>", None))

from pyqtgraph import PlotWidget