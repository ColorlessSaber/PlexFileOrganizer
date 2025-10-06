"""
Thread for creating the media folders in the selected directory
"""
from PySide6 import QtCore as qtc
from ..functions import video_file_condition
from ..classes import correct_media_file_format, DefaultThreadSignals
import os

class ScanExistingMediaFolder(qtc.QRunnable):

    class ThreadSignals(DefaultThreadSignals):
        finished = qtc.Signal(object) # overwritten to emit an object when thread is finished
        not_media_folder = qtc.Signal()

    def __init__(self, media_folder_information):
        super().__init__()
        self.media_folder_information = media_folder_information
        self.signals = self.ThreadSignals()

    @qtc.Slot()
    def run(self):
        """
        Initialize the thread
        """
        folder_and_file_patterns = correct_media_file_format.FolderAndFilePatterns()
        self.signals.progress.emit(25, "Scanning existing media folder...")

        with os.scandir(self.media_folder_information.directory) as directory_to_scan:
            for entry in directory_to_scan:
                if entry.is_file() and video_file_condition(entry.path) and not entry.name.startswith('.'):
                    self.media_folder_information.movie_or_tv = 'movie'
                elif entry.is_dir():
                    if folder_and_file_patterns.extra_folder_check(entry.name):
                        self.media_folder_information.extra_folders[entry.name] = True
                    elif folder_and_file_patterns.tv_show_season_folder_check(entry.name):
                        self.media_folder_information.number_of_seasons += 1
                    else:
                        pass
                else:
                    pass

        self.signals.progress.emit(100, "Scan complete!")
        self.signals.finished.emit(self.media_folder_information)