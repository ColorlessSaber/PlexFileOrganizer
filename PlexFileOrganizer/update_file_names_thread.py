"""
Thread for function file_name_updater
"""
from PlexFileOrganizer.functions import file_name_updater
from PySide6 import QtCore as qtc


class ThreadSignals(qtc.QObject):
    """
    The signals for the thread
    """
    finish = qtc.Signal(str)
    progress = qtc.Signal(int, str)


class UpdateFileNamesThread(qtc.QRunnable):
    """
    The thread for the file_name_updater function
    """
    def __init__(self, file_list, location):
        super().__init__()

        # variables
        self.file_list = file_list
        self.location = location
        self.signals = ThreadSignals

    @qtc.Slot()
    def run(self):
        """
        Initialize the thread
        :return:
        """
        file_name_updater(self.file_list, self.location)
