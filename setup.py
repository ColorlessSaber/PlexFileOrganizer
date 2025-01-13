"""
setup file
"""
import os
import sys

from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from PlexFileOrganizer import MainWindow

basedir = os.path.dirname(__file__)

if __name__ == '__main__':
    if (sys.version_info.major >= 3) and (sys.version_info.minor >= 12):
        app = qtw.QApplication(sys.argv)
        app.setWindowIcon(qtg.QIcon(os.path.join(basedir, 'Plex Media Organizer Icon.png')))
        mw = MainWindow()
        sys.exit(app.exec())    # doing this will pass appropriate exit codes to the OS, if the program crashes
    else:
        print('Need Python 3.12 or higher to run')
