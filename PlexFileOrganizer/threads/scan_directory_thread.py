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

    def __init__(self, directory_path):
        super().__init__()
        #TODO pass a value to files_in_extra_folders_are_not_formated
        self.files_in_extra_folders_are_not_formated = True # a flag that makes the function define all files in extra folders as not
        self.directory_path = directory_path
        self.mutex = qtc.QMutex()
        self.signals = ThreadSignals()

    @qtc.Slot()
    def run(self):
        """
        Initialize the thread

        :return:
        """
        extra_folder_format = re.compile(r"""
                                ^(trailer(s)?) | # trailers folder
                                (behind the scenes) | # behind the scenes folder
                                (deleted scenes) | # deleted scenes folder
                                (featurettes) | # featurettes folder
                                (interviews) | # interviews folder
                                (scenes) | # scenes folder
                                (shorts) | # shorts folder
                                (other) | # other folder
                                """, re.VERBOSE | re.IGNORECASE)
        media_file_list = []    # holds the media files that need to be updated

        self.mutex.lock()
        try:
            for entry in directory_scanner(self.directory_path):
                if any(entry.path.endswith(extension) for extension in ['.mkv', '.mp4', '.avi']):
                    if not correct_media_file_format(entry, self.files_in_extra_folders_are_not_formated):
                        media_file_list.append(MediaFile(entry.path))

        except OSError as e:
            self.signals.error.emit(e)

        finally:
            self.mutex.unlock()

            # check to see if the scan found media files that need to be updated.
            if media_file_list:
                self.signals.media_files_found.emit(media_file_list)
            else:
                self.signals.no_media_files_found.emit()
