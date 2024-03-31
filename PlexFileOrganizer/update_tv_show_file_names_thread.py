"""
Thread for updating the media files for a TV show
"""
from PlexFileOrganizer.functions import file_name_updater
from PySide6 import QtCore as qtc


class ThreadSignals(qtc.QObject):
    """
    The signals for the thread
    """
    finish = qtc.Signal(str)
    progress = qtc.Signal(int, str)


class UpdateTvShowFileNamesThread(qtc.QRunnable):
    """
    The thread for the file_name_updater function
    """
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
        file_list = []

        # create the new file names
        show_title = self.directory.split('/')[-2]
        season_number = self.directory.split('Season')[-1]

        for old_file_name, ep_num in zip(self.media_file_list, range(0, len(self.media_file_list))):
            # last entry is grabbing the file extension
            new_file_name = f"{show_title} - s{season_number.replace(' ', '')}e{ep_num}.{old_file_name.split('.')[-1]}"
            file_list.append([old_file_name, new_file_name])

        print(file_list)    # for testing for-loop above

        file_name_updater(file_list, self.directory)

        self.signals.finish.emit(
            'Show ' + show_title + ', ' + self.directory.split('/')[-1] + ' files have been renamed!'
        )
