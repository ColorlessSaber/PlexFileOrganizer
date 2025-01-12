"""
Thread for creating the media folders in the selected directory
"""
from PySide6 import QtCore as qtc
import os

class ThreadSignals(qtc.QObject):
    """
    The signals for thread
    """
    error = qtc.Signal(str)
    finish = qtc.Signal(str)
    progress = qtc.Signal(int, str)
    request_user_input_signal = qtc.Signal()

class CreateMediaFolderThread(qtc.QRunnable):

    def __init__(self, create_media_folder_selection):
        super().__init__()
        self.create_media_folder_selection = create_media_folder_selection
        self.wait_condition = qtc.QWaitCondition()
        self.mutex = qtc.QMutex()
        self.signals = ThreadSignals()
        self.user_confirmed_directory_exists = False

    @qtc.Slot()
    def run(self):
        """
        Initialize the thread
        :return:
        """
        self.mutex.lock()
        try:
            self.signals.progress.emit(10, 'Checking if Media Folder Exists.')
            media_folder_directory = self.create_media_folder_selection['directory'] + '/' + self.create_media_folder_selection['media title']
            an_extra_folder_was_created = False

            # check to see if the directory already has the media folder
            does_directory_exist = os.path.isdir(media_folder_directory)
            if does_directory_exist:
                self.signals.progress.emit(15, 'Media Folder found. Informing user.')
                self.signals.request_user_input_signal.emit()
                self.wait_condition.wait(self.mutex)

            if self.user_confirmed_directory_exists:
                self.signals.progress.emit(0, 'Canceling creation of Media Folder.')
            else:
                self.signals.progress.emit(20, 'Starting the process of creating Media Folder for: ' +
                                           self.create_media_folder_selection['media title'])

                ###
                # Create the Media Folder in the directory selected, along with the sub-folders
                ###
                os.mkdir(media_folder_directory)
                self.signals.progress.emit(40, '...Media folder created.')

                if self.create_media_folder_selection['movie or tv'] == 'tv':
                    # The plus one is to make sure it creates the correct number of season folders
                    for season_num in range(1, self.create_media_folder_selection['number of seasons']+1):
                        os.mkdir(media_folder_directory + '/' + 'Season ' + str(season_num))
                    self.signals.progress.emit(60, '...Season folder(s) created.')

                # iterate through the keys of the dict in the 'extra folder' entry. If entry in the sub-dict is true
                # create the folder, else pass.
                for extra_folders_key in self.create_media_folder_selection['extra folders']:
                    if self.create_media_folder_selection['extra folders'][extra_folders_key]:
                        os.mkdir(media_folder_directory + '/' + extra_folders_key)
                        an_extra_folder_was_created = True

                if an_extra_folder_was_created:
                    self.signals.progress.emit(80, '...Extra folder(s) created.')

                self.signals.progress.emit(100, 'Finished making Media Folder!')
        except OSError as e:
            self.signals.error.emit(e)

        finally:
            self.mutex.unlock()

    @qtc.Slot()
    def user_confirmation(self):
        """
        Receives confirmation from user that they understand directory exists.

        :return:
        """
        self.user_confirmed_directory_exists = True
        self.wait_condition.wakeAll()
