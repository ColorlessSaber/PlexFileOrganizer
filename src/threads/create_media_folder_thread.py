"""
Thread for creating the media folders in the selected directory
"""
import time
from PySide6 import QtCore as qtc
from ..classes import DefaultThreadSignals

class CreateMediaFolderThread(qtc.QRunnable):
    class ThreadSignals(DefaultThreadSignals):
        """
        The signals for thread
        """
        media_folder_already_exists = qtc.Signal()

    def __init__(self, media_folder_information):
        super().__init__()
        self.media_folder_information = media_folder_information
        self.signals = self.ThreadSignals()

    @qtc.Slot()
    def run(self) -> None:
        """
        Initialize the thread
        :return:
        """

        try:
            self.signals.progress.emit(10, 'Checking if Media Folder Exists...')
            if self.media_folder_information.check_if_media_folder_exists():
                time.sleep(1) # delay for one second so user sees the program is working.
                self.signals.progress.emit(0, 'Canceling creation of Media Folder.')
                self.signals.media_folder_already_exists.emit()
            else:
                time.sleep(1)  # delay for one second so user sees the program is working.
                self.signals.progress.emit(20, 'Folder does not exist. Starting the process of creating Media Folder for: ' +
                                           self.media_folder_information.media_title)

                self.signals.progress.emit(30, '-- Creating media folder.')
                time.sleep(1)  # delay for one second so user sees the program is working.
                self.media_folder_information.generate_media_folder()
                self.signals.progress.emit(40, '-- Folder created.')

                if self.media_folder_information.media_type == 'tv':
                    self.signals.progress.emit(50, '-- Creating season folder(s).')
                    time.sleep(1)  # delay for one second so user sees the program is working.
                    self.media_folder_information.generate_seasons()
                    self.signals.progress.emit(60, '-- Season folder(s) created.')

                if self.media_folder_information.check_if_new_extra_folders_are_needed():
                    self.signals.progress.emit(70, '-- Creating extra folder(s).')
                    time.sleep(1)  # delay for one second so user sees the program is working.
                    self.media_folder_information.generate_new_extra_folders()
                    self.signals.progress.emit(80, '-- Extra folder(s) created.')
                else:
                    self.signals.progress.emit(80, '-- No extra folder(s) needed to be created.')
                    time.sleep(1)  # delay for one second so user sees the program is working.

                self.signals.finished.emit()
                self.signals.progress.emit(100, 'Finished generating Media Folder!')

        except OSError as e:
            self.signals.error.emit(e)

        except BaseException as e:
            self.signals.error.emit(e)
