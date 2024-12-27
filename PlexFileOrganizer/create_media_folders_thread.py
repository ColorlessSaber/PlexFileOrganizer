"""
Thread for creating the media folders in the selected directory
"""
from PySide6 import QtCore as qtc

class ThreadSignals(qtc.QObject):
    """
    The signals for thread
    """
    error = qtc.Signal(str)
    finish = qtc.Signal(str)
    progress = qtc.Signal(int, str)
    request_user_input_signal = qtc.Signal(str)

class CreateMediaFoldersThread(qtc.QRunnable):

    def __init__(self, create_media_folders_selection):
        super().__init__()
        self.create_media_folders_selection = create_media_folders_selection
        self.wait_condition = qtc.QWaitCondition()
        self.mutex = qtc.QMutex()
        self.signals = ThreadSignals()
        self.should_pause = False

    @qtc.Slot()
    def run(self):
        """
        Initialize the thread
        :return:
        """
        self.mutex.lock()
        print('hi')
        """
        
        """
        self.mutex.unlock()

    @qtc.Slot()
    def user_input(self):
        """
        Receives input from user.

        :return:
        """
        print('hi')
        self.wait_condition.wakeAll()
