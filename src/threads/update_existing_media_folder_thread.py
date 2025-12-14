"""
Thread for updating existing media folder
"""
import time
from PySide6 import QtCore as qtc
from ..classes import DefaultThreadSignals

class UpdateExistingMediaFolderThread(qtc.QRunnable):
    class ThreadSignals(DefaultThreadSignals):
        """
        The signals for thread
        """

    def __init__(self, info_of_media_folder):
        super().__init__()
        self.info_of_media_folder = info_of_media_folder
        self.signals = self.ThreadSignals()

    @qtc.Slot()
    def run(self) -> None:
        """
        Initialize the thread
        """
        try:
            self.signals.progress.emit(17, "Starting to update existing media folder: " +
                                       self.info_of_media_folder.media_title)
            time.sleep(1)  # delay for a second so the user sees the program is working.
            if self.info_of_media_folder.media_type == 'tv':
                self.signals.progress.emit(24, '-- Generating more season folder(s).')
                time.sleep(1)  # delay for a second so the user sees the program is working.
                self.info_of_media_folder.generate_new_season_folders()
                self.signals.progress.emit(41, "-- New season folder(s) generated.")

            self.signals.progress.emit(58, "-- Generating extra folder(s).")
            time.sleep(1)  # delay for a second so the user sees the program is working.
            self.info_of_media_folder.generate_new_extra_folders()
            self.signals.progress.emit(75, "-- Extra folder(s) generated.")

            self.signals.progress.emit(100, "Update of Media Folder completed!")
            self.signals.finished.emit()
        except OSError as e:
            self.signals.error.emit(e)
        except BaseException as e:
            self.signals.error.emit(e)