"""
Thread for updating the media files for a movie
"""
from PlexFileOrganizer.functions import file_name_updater
from PySide6 import QtCore as qtc


class ThreadSignals(qtc.QObject):
    """
    The signals for the thread
    """
    finish = qtc.Signal(str)
    progress = qtc.Signal(int, str)


class UpdateMovieFileNameThread(qtc.QRunnable):

    def __init__(self, media_file_list, directory):
        super().__init__()

        # variables
        self.media_file_list = media_file_list
        self.directory = directory
        self.signals = ThreadSignals()

    @qtc.Slot()
    def run(self):
        """
        Initialize the thread
        :return:
        """
        movie_title = self.directory.split('/')[-1]
        new_file_name = f"{movie_title}.{self.media_file_list[0].split('.')[-1]}"   # last entry in string is for grabbing the file extension
        file_name_updater([[self.media_file_list[0], new_file_name]], self.directory)

        self.signals.finish.emit(
            'Movie ' + movie_title + ' file have been renamed!'
        )
