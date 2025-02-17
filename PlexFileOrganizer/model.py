"""
The back-end of the Plex File Organizer
"""
import os
from PySide6 import QtCore as qtc
from PlexFileOrganizer.threads import ScanDirectoryThread, CreateMediaFolderThread
from PlexFileOrganizer.functions import media_file_check


class Model(qtc.QObject):

    thread_pool = qtc.QThreadPool()

    user_input_request_signal = qtc.Signal()
    user_input_response_signal = qtc.Signal()
    error_message_signal = qtc.Signal(str)
    update_progress_signal = qtc.Signal(int, str)

    analysis_of_media_folder_complete_signal = qtc.Signal(object)
    update_file_names_complete_signal = qtc.Signal(str)

    @qtc.Slot(object)
    def start_create_media_folder_thread(self, media_folder_selection):
        """
        Starts the thread to create the folder(s) the user wishes to make.

        :param media_folder_selection: Dataclass MediaFolder, holding the user inputs and selections.
        :return:
        """
        create_media_folder_thread = CreateMediaFolderThread(media_folder_selection)
        create_media_folder_thread.signals.request_user_input_signal.connect(self.user_input_request_signal)
        create_media_folder_thread.signals.progress.connect(self.update_progress_signal)
        #TODO add in signal to launch popup to inform user the task is done.
        self.user_input_response_signal.connect(create_media_folder_thread.user_confirmation)
        self.thread_pool.start(create_media_folder_thread)

    @qtc.Slot(str)
    def start_scan_of_directory_thread(self, directory_path):
        """
        Starts the thread to scan the selected directory.

        :param directory_path: The directory path the user wishes to scan
        :return:
        """
        scan_directory_thread = ScanDirectoryThread(directory_path)
        scan_directory_thread.signals.progress.connect(self.update_progress_signal)
        self.thread_pool.start(scan_directory_thread)

    @qtc.Slot(str)
    def complete_update_file_names(self, completed_message):
        """
        Signal for completion of either UpdateTvShowFileNamesThread or UpdateMovieFileNameThread

        :return:
        """
        self.update_file_names_complete_signal.emit(completed_message)

    @qtc.Slot(str)
    def error_detected(self, error_message):
        """
        Signal when ran into error

        :param error_message: error message string
        :return:
        """
        self.error_message_signal.emit(error_message)

    @qtc.Slot(str)
    def analyze_media_folder(self, directory):
        """
        OLD CODE! WILL BE REMOVED SHORTLY!

        Checks the directory to see if it's a media folder for a movie or TV show. If it passes: creates a list of the
        media file(s) in the directory given; and determines if the directory is for a movie or TV show,
        the tile of the show and if a TV show the TV show's season number.

        :param directory: Location of the media file(s)
        :return: a tuple with the following information (list of media file(s), media type, title of show)
        """
        media_file_list = []

        # determine if directory is a media folder
        if any(i in directory.lower() for i in ['movies', 'tv shows']):

            # create a list of the media files in directory
            for item in os.listdir(directory):
                if any(item.endswith(extension) for extension in ['.mkv', '.mp4', '.avi']):
                    media_file_list.append(item)

            if media_file_list:

                # Check to see if media file(s) have already been updated
                results = media_file_check(media_file_list, directory)
                match results:
                    case 'Files Not Updated':
                        # see if the directory is for a movie or TV show
                        if 'season' in directory.lower():
                            media_type = 'TV Show'

                            # grab the show title and season number
                            show_title = directory.split('/')[-2] + ', ' + directory.split('/')[-1]

                        else:
                            media_type = 'Movie'

                            # grab the movie title
                            show_title = directory.split('/')[-1]

                        self.analyzation_of_media_folder_complete_signal.emit((media_file_list, media_type, show_title))
                    case 'Files Updated':
                        self.error_message_signal.emit('Files in directory are already updated: ' + directory)
            else:
                self.error_message_signal.emit('No media was found in folder: ' + directory)
        else:
            self.error_message_signal.emit('Folder selected is not a media folder. ' + directory)
