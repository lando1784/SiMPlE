# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtView.ui'
#
# Created: Sat Aug 30 00:24:59 2014
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
        facewindow.resize(897, 655)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../smfsmanager/D_mica.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        facewindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(facewindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.grafo = PlotWidget(self.centralwidget)
        self.grafo.setGeometry(QtCore.QRect(0, 0, 751, 551))
        self.grafo.setToolTip(_fromUtf8(""))
        self.grafo.setStatusTip(_fromUtf8(""))
        self.grafo.setWhatsThis(_fromUtf8(""))
        self.grafo.setObjectName(_fromUtf8("grafo"))
        self.slide1 = QtGui.QScrollBar(self.centralwidget)
        self.slide1.setEnabled(True)
        self.slide1.setGeometry(QtCore.QRect(750, 0, 16, 551))
        self.slide1.setMinimum(1)
        self.slide1.setMaximum(1)
        self.slide1.setTracking(False)
        self.slide1.setOrientation(QtCore.Qt.Vertical)
        self.slide1.setObjectName(_fromUtf8("slide1"))
        self.slide2 = QtGui.QDial(self.centralwidget)
        self.slide2.setEnabled(True)
        self.slide2.setGeometry(QtCore.QRect(790, 555, 71, 71))
        self.slide2.setMinimum(1)
        self.slide2.setMaximum(1)
        self.slide2.setTracking(True)
        self.slide2.setObjectName(_fromUtf8("slide2"))
        self.griglia = QtGui.QGraphicsView(self.centralwidget)
        self.griglia.setEnabled(True)
        self.griglia.setGeometry(QtCore.QRect(770, 10, 121, 511))
        self.griglia.setObjectName(_fromUtf8("griglia"))
        self.labFilename = QtGui.QLabel(self.centralwidget)
        self.labFilename.setGeometry(QtCore.QRect(480, 10, 261, 16))
        self.labFilename.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labFilename.setObjectName(_fromUtf8("labFilename"))
        self.slide3 = QtGui.QSpinBox(self.centralwidget)
        self.slide3.setGeometry(QtCore.QRect(770, 524, 121, 27))
        self.slide3.setMinimum(1)
        self.slide3.setMaximum(1)
        self.slide3.setObjectName(_fromUtf8("slide3"))
        self.bAddFiles = QtGui.QPushButton(self.centralwidget)
        self.bAddFiles.setGeometry(QtCore.QRect(650, 560, 89, 27))
        self.bAddFiles.setObjectName(_fromUtf8("bAddFiles"))
        self.bAddDir = QtGui.QPushButton(self.centralwidget)
        self.bAddDir.setGeometry(QtCore.QRect(540, 560, 89, 27))
        self.bAddDir.setObjectName(_fromUtf8("bAddDir"))
        facewindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(facewindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 897, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        facewindow.setMenuBar(self.menubar)

        self.retranslateUi(facewindow)
        QtCore.QMetaObject.connectSlotsByName(facewindow)

    def retranslateUi(self, facewindow):
        facewindow.setWindowTitle(_translate("facewindow", "MainWindow", None))
        self.labFilename.setText(_translate("facewindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">FILENAME</span></p></body></html>", None))
        self.bAddFiles.setText(_translate("facewindow", "Add Files", None))
        self.bAddDir.setText(_translate("facewindow", "Add DIR", None))

from pyqtgraph import PlotWidget
