"""
Thread for creating the media folders in the selected directory
"""
from PySide6 import QtCore as qtc
from PlexFileOrganizer.functions import correct_media_file_format, video_file_condition
import os

class ThreadSignals(qtc.QObject):
    """
    The signals for thread
    """
    error = qtc.Signal(str)
    progress = qtc.Signal(int, str)
    scan_failed = qtc.Signal()
    scan_completed = qtc.Signal(object)

class ScanExistingMediaFolder(qtc.QRunnable):

    def __init__(self, media_folder_information):
        super().__init__()
        self.media_folder_information = media_folder_information
        self.signals = ThreadSignals()

    @qtc.Slot()
    def run(self):
        """
        Initialize the thread
        """
        folder_and_file_patterns = correct_media_file_format.FolderAndFilePatterns()
        self.signals.progress.emit(10, "Scanning existing media folder...")

        with os.scandir(self.media_folder_information.directory) as directory_to_scan:
            for entry in directory_to_scan:
                if entry.is_file() and video_file_condition(entry.path) and not entry.name.startswith('.'):
                    print(entry)
                elif entry.is_dir() and (folder_and_file_patterns.extra_folder_check(entry.path) or folder_and_file_patterns.tv_show_season_folder_check(entry.path)):
                    print(entry)
                else:
                    pass