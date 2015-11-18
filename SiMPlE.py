from GUIs.SiMPlE_MainGUI import *
import sys
CURRMOD = list(sys.modules.keys())
try:
    ENV = 'PyQt5'
    CURRMOD.index(ENV)
    from PyQt5.QtWidgets import QApplication
except:
    ENV = 'PyQt4'
    CURRMOD.index(ENV)
    from PyQt4.QtGui import QApplication

from GUIs.SiMPlE_MainGUI_Engine import SiMPlE_main

try:
    VERBOSE = sys.argv[1] == '-v' or sys.argv[1] == '--verbose'
except:
    VERBOSE = False

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    mainWin = SiMPlE_main(verbose = VERBOSE)
    mainWin.show()
    
    app.exec_()
