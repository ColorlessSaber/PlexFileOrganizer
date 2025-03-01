"""
Thread for scanning the directory user selected
"""
import re
from PySide6 import QtCore as qtc
from PlexFileOrganizer.functions import directory_scanner, correct_media_file_format, MediaFile

class ThreadSignals(qtc.QObject):
    """
    The signals for thread
    """
    error = qtc.Signal(str)
    media_files_found = qtc.Signal(object)
    no_media_files_found = qtc.Signal()
    progress = qtc.Signal(int, str)

class ScanDirectoryThread(qtc.QRunnable):

    def __init__(self, directory_path, current_media_file_list, files_in_extra_folders_are_formated):
        """

        :param directory_path: Directory to scan
        :param current_media_file_list: The media files that were found in the previous directory scan
        :param files_in_extra_folders_are_formated: a flag that makes the function define all files in extra folders are
        formated correctly or not. True - formated correctly, False - not formated correctly.
        """
        super().__init__()
        self.files_in_extra_folders_are_formated = files_in_extra_folders_are_formated
        self.directory_path = directory_path
        self.current_media_file_list = current_media_file_list
        self.mutex = qtc.QMutex()
        self.signals = ThreadSignals()

    @qtc.Slot()
    def run(self):
        """
        Initialize the thread

        :return:
        """
        scan_media_file_list = []    # holds the media files that were found that need to be updated

        self.mutex.lock()
        try:
            for entry in directory_scanner(self.directory_path):
                if any(entry.path.endswith(extension) for extension in ['.mkv', '.mp4', '.avi']):
                    if not correct_media_file_format(entry, self.files_in_extra_folders_are_formated):
                        scan_media_file_list.append(MediaFile(entry.path))

            # compare current_media_file_list to scan_media_file_list
            # if there is a media file in scan_media_file_list, append it to current_media_file_list
            for media_file in scan_media_file_list:
                if media_file not in self.current_media_file_list:
                    self.current_media_file_list.append(media_file)

        except OSError as e:
            self.signals.error.emit(e)

        finally:
            self.mutex.unlock()

            # check to see if any media files were found
            if self.current_media_file_list:
                self.signals.media_files_found.emit(self.current_media_file_list)
            else:
                self.signals.no_media_files_found.emit()
