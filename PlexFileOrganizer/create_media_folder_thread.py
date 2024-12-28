"""
Thread for creating the media folders in the selected directory
"""
from PySide6 import QtCore as qtc
import os

class ThreadSignals(qtc.QObject):
    """
    The signals for thread
    """
    error = qtc.Signal(str)
    finish = qtc.Signal(str)
    progress = qtc.Signal(int, str)
    request_user_input_signal = qtc.Signal()

class CreateMediaFolderThread(qtc.QRunnable):

    def __init__(self, create_media_folder_selection):
        super().__init__()
        self.create_media_folder_selection = create_media_folder_selection
        self.wait_condition = qtc.QWaitCondition()
        self.mutex = qtc.QMutex()
        self.signals = ThreadSignals()
        self.user_confirmed_directory_exists = False

    @qtc.Slot()
    def run(self):
        """
        Initialize the thread
        :return:
        """
        self.mutex.lock()
        self.signals.progress.emit(10, 'Checking if Media Folder Exists.')

        # check to see if the directory already has the media folder
        does_directory_exist = os.path.isdir(self.create_media_folder_selection['directory'] + '/' + self.create_media_folder_selection['media title'])
        if does_directory_exist:
            self.signals.progress.emit(10, 'Media Folder found. Informing user.')
            self.signals.request_user_input_signal.emit()
            self.wait_condition.wait(self.mutex)

        if self.user_confirmed_directory_exists:
            self.signals.progress.emit(0, 'Canceling creation of Media Folder.')
        else:
            self.signals.progress.emit(20, 'Starting the process of creating Media Folder.')
            "code"
            self.signals.progress.emit(100, 'Finished making Media Folder!')

        self.mutex.unlock()

    @qtc.Slot()
    def user_input(self):
        """
        Receives input from user.

        :return:
        """
        self.user_confirmed_directory_exists = True
        self.wait_condition.wakeAll()
