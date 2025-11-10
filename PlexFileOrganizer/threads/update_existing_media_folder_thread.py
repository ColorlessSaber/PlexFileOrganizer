"""
Thread for updating existing media folder
"""
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
    def run(self):
        """
        Initialize the thread
        """
        self.signals.progress.emit(25, "Starting to update existing media folder:")
        try:
            if self.info_of_media_folder.media_type == 'tv':
                self.info_of_media_folder.generate_new_season_folders()
                self.signals.progress.emit(50, "...New Season folder(s) generated.")

            self.info_of_media_folder.generate_new_extra_folders()
            self.signals.progress.emit(75, "...Extra folder(s) generated.")

            self.signals.progress.emit(100, "Update of Media Folder completed!")
            self.signals.finished.emit()
        except OSError as e:
            self.signals.error.emit(e)