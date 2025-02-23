"""
Thread for scanning the directory user selected
"""
from collections import deque
from PySide6 import QtCore as qtc
from PlexFileOrganizer.functions import directory_scanner, correct_media_file_format, MediaFile

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
        self.directory_path = deque([directory_path])
        self.mutex = qtc.QMutex()
        self.signals = ThreadSignals()

    @qtc.Slot()
    def run(self):
        """
        Initialize the thread

        :return:
        """
        media_file_list = []    # holds the media files that need to be updated

        self.mutex.lock()
        for entry in directory_scanner(self.directory_path):
            if not correct_media_file_format(entry.path):
                media_file_list.append(entry.path)

        self.mutex.unlock()
