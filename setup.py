"""
setup file
"""
import sys
from PySide6 import QtWidgets as qtw
from app import MainWindow

if __name__ == '__main__':
    if (sys.version_info.major >= 3) and (sys.version_info.minor >= 12):
        app = qtw.QApplication(sys.argv)
        mw = MainWindow()
        sys.exit(app.exec())
    else:
        print('Need Python 3.12 or higher to run')
