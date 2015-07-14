# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtView.ui'
#
# Created: Mon Jul 13 19:17:27 2015
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
        facewindow.resize(1027, 696)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../smfsmanager/D_mica.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        facewindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(facewindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.grafo = PlotWidget(self.centralwidget)
        self.grafo.setToolTip(_fromUtf8(""))
        self.grafo.setStatusTip(_fromUtf8(""))
        self.grafo.setWhatsThis(_fromUtf8(""))
        self.grafo.setObjectName(_fromUtf8("grafo"))
        self.gridLayout.addWidget(self.grafo, 0, 0, 1, 2)
        self.slide1 = QtGui.QScrollBar(self.centralwidget)
        self.slide1.setEnabled(True)
        self.slide1.setMinimum(1)
        self.slide1.setMaximum(1)
        self.slide1.setTracking(False)
        self.slide1.setOrientation(QtCore.Qt.Vertical)
        self.slide1.setObjectName(_fromUtf8("slide1"))
        self.gridLayout.addWidget(self.slide1, 0, 2, 1, 1)
        self.griglia = QtGui.QGraphicsView(self.centralwidget)
        self.griglia.setEnabled(True)
        self.griglia.setObjectName(_fromUtf8("griglia"))
        self.gridLayout.addWidget(self.griglia, 0, 3, 1, 1)
        self.slide2 = QtGui.QDial(self.centralwidget)
        self.slide2.setEnabled(True)
        self.slide2.setMinimum(1)
        self.slide2.setMaximum(1)
        self.slide2.setTracking(True)
        self.slide2.setObjectName(_fromUtf8("slide2"))
        self.gridLayout.addWidget(self.slide2, 1, 3, 1, 1)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.line_3 = QtGui.QFrame(self.centralwidget)
        self.line_3.setLineWidth(6)
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout_3.addWidget(self.line_3, 0, 5, 3, 1)
        self.kNumDbl = QtGui.QDoubleSpinBox(self.centralwidget)
        self.kNumDbl.setMaximum(1000.0)
        self.kNumDbl.setObjectName(_fromUtf8("kNumDbl"))
        self.gridLayout_3.addWidget(self.kNumDbl, 0, 7, 1, 1)
        self.speedNumDbl = QtGui.QDoubleSpinBox(self.centralwidget)
        self.speedNumDbl.setMaximum(1000.0)
        self.speedNumDbl.setObjectName(_fromUtf8("speedNumDbl"))
        self.gridLayout_3.addWidget(self.speedNumDbl, 2, 7, 1, 1)
        self.bAddDir = QtGui.QPushButton(self.centralwidget)
        self.bAddDir.setObjectName(_fromUtf8("bAddDir"))
        self.gridLayout_3.addWidget(self.bAddDir, 0, 0, 1, 1)
        self.bAddFiles = QtGui.QPushButton(self.centralwidget)
        self.bAddFiles.setObjectName(_fromUtf8("bAddFiles"))
        self.gridLayout_3.addWidget(self.bAddFiles, 1, 0, 1, 1)
        self.convr9Btn = QtGui.QPushButton(self.centralwidget)
        self.convr9Btn.setObjectName(_fromUtf8("convr9Btn"))
        self.gridLayout_3.addWidget(self.convr9Btn, 2, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_3.addWidget(self.label_4, 0, 6, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 0, 1, 1, 2)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 1, 1, 1, 1)
        self.labFilename = QtGui.QLabel(self.centralwidget)
        self.labFilename.setObjectName(_fromUtf8("labFilename"))
        self.gridLayout_3.addWidget(self.labFilename, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_3.addWidget(self.label_3, 2, 1, 1, 1)
        self.labelNumber = QtGui.QLabel(self.centralwidget)
        self.labelNumber.setObjectName(_fromUtf8("labelNumber"))
        self.gridLayout_3.addWidget(self.labelNumber, 2, 2, 1, 1)
        self.nmVNumDbl = QtGui.QDoubleSpinBox(self.centralwidget)
        self.nmVNumDbl.setMaximum(1000.0)
        self.nmVNumDbl.setObjectName(_fromUtf8("nmVNumDbl"))
        self.gridLayout_3.addWidget(self.nmVNumDbl, 1, 7, 1, 1)
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_3.addWidget(self.label_5, 1, 6, 1, 1)
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_3.addWidget(self.label_6, 2, 6, 1, 1)
        self.updateKBtn = QtGui.QPushButton(self.centralwidget)
        self.updateKBtn.setObjectName(_fromUtf8("updateKBtn"))
        self.gridLayout_3.addWidget(self.updateKBtn, 0, 8, 1, 1)
        self.updateNmVBtn = QtGui.QPushButton(self.centralwidget)
        self.updateNmVBtn.setObjectName(_fromUtf8("updateNmVBtn"))
        self.gridLayout_3.addWidget(self.updateNmVBtn, 1, 8, 1, 1)
        self.updateSpeedBtn = QtGui.QPushButton(self.centralwidget)
        self.updateSpeedBtn.setObjectName(_fromUtf8("updateSpeedBtn"))
        self.gridLayout_3.addWidget(self.updateSpeedBtn, 2, 8, 1, 1)
        self.updateAllKBtn = QtGui.QPushButton(self.centralwidget)
        self.updateAllKBtn.setObjectName(_fromUtf8("updateAllKBtn"))
        self.gridLayout_3.addWidget(self.updateAllKBtn, 0, 9, 1, 1)
        self.updateAllNmVBtn = QtGui.QPushButton(self.centralwidget)
        self.updateAllNmVBtn.setObjectName(_fromUtf8("updateAllNmVBtn"))
        self.gridLayout_3.addWidget(self.updateAllNmVBtn, 1, 9, 1, 1)
        self.updateAllSpeedBtn = QtGui.QPushButton(self.centralwidget)
        self.updateAllSpeedBtn.setObjectName(_fromUtf8("updateAllSpeedBtn"))
        self.gridLayout_3.addWidget(self.updateAllSpeedBtn, 2, 9, 1, 1)
        self.autoFitBtn = QtGui.QPushButton(self.centralwidget)
        self.autoFitBtn.setObjectName(_fromUtf8("autoFitBtn"))
        self.gridLayout_3.addWidget(self.autoFitBtn, 0, 13, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.alignBtn = QtGui.QPushButton(self.centralwidget)
        self.alignBtn.setObjectName(_fromUtf8("alignBtn"))
        self.horizontalLayout.addWidget(self.alignBtn)
        self.rejectBtn = QtGui.QPushButton(self.centralwidget)
        self.rejectBtn.setObjectName(_fromUtf8("rejectBtn"))
        self.horizontalLayout.addWidget(self.rejectBtn)
        self.gridLayout_3.addLayout(self.horizontalLayout, 2, 13, 1, 1)
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setLineWidth(6)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout_3.addWidget(self.line_2, 0, 11, 3, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 3, 1, 1)
        self.line_4 = QtGui.QFrame(self.centralwidget)
        self.line_4.setLineWidth(6)
        self.line_4.setFrameShape(QtGui.QFrame.VLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.gridLayout_3.addWidget(self.line_4, 0, 10, 3, 1)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setLineWidth(6)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_3.addWidget(self.line, 0, 4, 3, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 12, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.manSelBtn = QtGui.QPushButton(self.centralwidget)
        self.manSelBtn.setObjectName(_fromUtf8("manSelBtn"))
        self.horizontalLayout_2.addWidget(self.manSelBtn)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.horizontalLayout_2.setStretch(0, 3)
        self.horizontalLayout_2.setStretch(1, 1)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 1, 13, 1, 1)
        self.gridLayout_3.setColumnStretch(0, 2)
        self.gridLayout_3.setColumnStretch(1, 2)
        self.gridLayout_3.setColumnStretch(2, 1)
        self.gridLayout_3.setColumnStretch(3, 1)
        self.gridLayout_3.setColumnStretch(4, 1)
        self.gridLayout_3.setColumnStretch(5, 1)
        self.gridLayout_3.setColumnStretch(6, 2)
        self.gridLayout_3.setColumnStretch(7, 3)
        self.gridLayout_3.setColumnStretch(8, 2)
        self.gridLayout_3.setColumnStretch(9, 2)
        self.gridLayout_3.setColumnStretch(10, 1)
        self.gridLayout_3.setColumnStretch(11, 1)
        self.gridLayout_3.setColumnStretch(12, 1)
        self.gridLayout_3.setColumnStretch(13, 4)
        self.gridLayout.addLayout(self.gridLayout_3, 1, 0, 1, 2)
        self.gridLayout.setColumnStretch(0, 4)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)
        facewindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(facewindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1027, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        facewindow.setMenuBar(self.menubar)

        self.retranslateUi(facewindow)
        QtCore.QMetaObject.connectSlotsByName(facewindow)

    def retranslateUi(self, facewindow):
        facewindow.setWindowTitle(_translate("facewindow", "MainWindow", None))
        self.bAddDir.setText(_translate("facewindow", "Add DIR", None))
        self.bAddFiles.setText(_translate("facewindow", "Add Files", None))
        self.convr9Btn.setText(_translate("facewindow", "Convert R9 files", None))
        self.label_4.setText(_translate("facewindow", "k [N/nm]", None))
        self.label.setText(_translate("facewindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Current curve</span></p></body></html>", None))
        self.label_2.setText(_translate("facewindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Name</span></p></body></html>", None))
        self.labFilename.setText(_translate("facewindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">//</span></p></body></html>", None))
        self.label_3.setText(_translate("facewindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Number</span></p></body></html>", None))
        self.labelNumber.setText(_translate("facewindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">0</span></p></body></html>", None))
        self.label_5.setText(_translate("facewindow", "Sensitivity [nm/V]", None))
        self.label_6.setText(_translate("facewindow", "Speed [nm/s]", None))
        self.updateKBtn.setText(_translate("facewindow", "UPDATE", None))
        self.updateNmVBtn.setText(_translate("facewindow", "UPDATE", None))
        self.updateSpeedBtn.setText(_translate("facewindow", "UPDATE", None))
        self.updateAllKBtn.setText(_translate("facewindow", "UPDATE ALL", None))
        self.updateAllNmVBtn.setText(_translate("facewindow", "UPDATE ALL", None))
        self.updateAllSpeedBtn.setText(_translate("facewindow", "UPDATE ALL", None))
        self.autoFitBtn.setText(_translate("facewindow", "Automatic fit", None))
        self.alignBtn.setText(_translate("facewindow", "Align", None))
        self.rejectBtn.setText(_translate("facewindow", "Reject", None))
        self.manSelBtn.setText(_translate("facewindow", "Manual selection", None))
        self.pushButton.setText(_translate("facewindow", "Cancel", None))

from pyqtgraph import PlotWidget
