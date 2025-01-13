"""
Thread for creating the media folders in the selected directory
"""
import os
from collections import Counter

from PySide6 import QtCore as qtc

class ThreadSignals(qtc.QObject):
    """
    The signals for thread
    """
    error = qtc.Signal(str)
    finish = qtc.Signal(str)
    progress = qtc.Signal(int, str)
    request_user_input_signal = qtc.Signal()

class CreateMediaFolderThread(qtc.QRunnable):

    def __init__(self, media_folder_information):
        super().__init__()
        self.media_folder_information = media_folder_information
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
        try:
            self.signals.progress.emit(10, 'Checking if Media Folder Exists.')
            if self.media_folder_information.check_if_media_folder_exists():
                self.signals.progress.emit(15, 'Media Folder found. Informing user.')
                self.signals.request_user_input_signal.emit()
                self.wait_condition.wait(self.mutex)

            if self.user_confirmed_directory_exists:
                self.signals.progress.emit(0, 'Canceling creation of Media Folder.')
            else:
                self.signals.progress.emit(20, 'Starting the process of creating Media Folder for: ' +
                                           self.media_folder_information.media_title)
                self.media_folder_information.generate_media_folder()
                self.signals.progress.emit(40, '...Media folder created.')

                if self.media_folder_information.movie_or_tv == 'tv':
                    self.media_folder_information.generate_seasons()
                    self.signals.progress.emit(60, '...Season folder(s) created.')

                an_extra_folder_was_created = self.media_folder_information.generate_extra_folders()
                if an_extra_folder_was_created:
                    self.signals.progress.emit(80, '...Extra folder(s) created.')

                self.signals.progress.emit(100, 'Finished making Media Folder!')

        except OSError as e:
            self.signals.error.emit(e)

        finally:
            self.mutex.unlock()

    @qtc.Slot()
    def user_confirmation(self):
        """
        Receives confirmation from user that they understand directory exists.

        :return:
        """
        self.user_confirmed_directory_exists = True
        self.wait_condition.wakeAll()
