"""
Thread for Auto Update Media Files
"""
from PySide6 import QtCore as qtc
from PlexFileOrganizer.functions import directory_scanner, correct_media_file_format

class ThreadSignals(qtc.QObject):
    """
    The signals for the thread
    """
    error = qtc.Signal(str)
    progress = qtc.Signal(int, str)

class AutoUpdateMediaFilesThread(qtc.QRunnable):

    def __init__(self, directory_and_options):
        """

        :param directory_and_options: The directory that contains the directory user selected, and
        other selectable options.
        """
        super().__init__()
        self.directory_and_options = directory_and_options
        self.signals = ThreadSignals()

    @qtc.Slot()
    def run(self):
        try:
            print('auto update thread')
            print(self.directory_and_options)
        except OSError as e:
            self.signals.error.emit(e)