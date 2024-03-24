"""
setup file
"""
import sys
from PlexFileOrganizer import MainWindow
from PySide6 import QtWidgets as qtw


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())    # doing this will pass appropriate exit codes to the OS, if the program crashes
