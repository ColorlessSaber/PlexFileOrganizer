"""
Thread for scanning the directory user selected
"""
from PySide6 import QtCore as qtc

class ThreadSignals(qtc.QObject):
    """
    The signals for thread
    """
    error = qtc.Signal(str)
    finish = qtc.Signal(str)
    progress = qtc.Signal(int, str)

class ScanDirectoryThread(qtc.QRunnable):

    def __init__(self, directory_path):
        super().__init__()
        self.directory_path = directory_path
        self.mutex = qtc.QMutex()
        self.signals = ThreadSignals()

    @qtc.Slot()
    def run(self):
        """
        Initialize the thread

        :return:
        """
        self.mutex.lock()
        print("Scanning directory {}!".format(self.directory_path))
        self.mutex.unlock()
