"""
setup file
"""
import sys
from PlexFileOrganizer import MainWindow
from PySide6 import QtWidgets as qtw


if __name__ == '__main__':
    if (sys.version_info.major >= 3) and (sys.version_info.minor >= 12):
        app = qtw.QApplication(sys.argv)
        mw = MainWindow()
        sys.exit(app.exec())    # doing this will pass appropriate exit codes to the OS, if the program crashes
    else:
        print('Need Python 3.12 or higher to run')
