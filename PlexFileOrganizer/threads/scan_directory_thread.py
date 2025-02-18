"""
Thread for scanning the directory user selected
"""
import re
from PySide6 import QtCore as qtc
from PlexFileOrganizer.functions import directory_scanner
from PlexFileOrganizer.functions import MediaFile

class ThreadSignals(qtc.QObject):
    """
    The signals for thread
    """
    error = qtc.Signal(str)
    finish = qtc.Signal(str)
    progress = qtc.Signal(int, str)

class ScanDirectoryThread(qtc.QRunnable):

    def __init__(self, directory_path):
        super().__init__()
        self.folders_to_check = [directory_path]
        self.mutex = qtc.QMutex()
        self.signals = ThreadSignals()

    @qtc.Slot()
    def run(self):
        """
        Initialize the thread

        :return:
        """
        check_media_file_tv_show_formate = re.compile(r"""
        ^.+   # wildcard to handle name of show
        \s  
        -
        \s
        s\d+e\d+(-e\d+)?  # season, episode number and possible multiple episode
        \.\w+ # file extension
        """, re.VERBOSE | re.IGNORECASE)
        media_file_list = []    # holds the media files that need to be updated

        self.mutex.lock()
        while self.folders_to_check:    # keep iterating through the folders until there is no more to check
            for entry in directory_scanner(self.folders_to_check[0]):
                if entry.is_dir():
                    #print('directory! {}'.format(entry.name))  # debugging
                    self.folders_to_check.append(entry.path)
                elif entry.is_file():
                    #print('file! {}'.format(entry.name))   # debugging
                    if any(entry.name.endswith(extension) for extension in ['.mkv', '.mp4', '.avi']):
                        if re.match(r'Season\s\d', entry.path.split('/')[-2]):  # media folder is a tv show
                            if not check_media_file_tv_show_formate.match(entry.name):  # if media file is not formated for show, add it to the list
                                media_file_list.append(MediaFile(entry.path))

                        else:   # media folder is movie
                            if entry.path.split('/')[-2] in entry.name: # if media file is not formated for movie, add it to the list
                                media_file_list.append(MediaFile(entry.path))

            self.folders_to_check.pop(0)    # remove the last folder that was checked.
        self.mutex.unlock()
