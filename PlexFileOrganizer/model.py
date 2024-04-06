"""
The back-end of the Plex File Organizer
"""
import os
from PySide6 import QtCore as qtc
from PlexFileOrganizer.update_tv_show_file_names_thread import UpdateTvShowFileNamesThread
from PlexFileOrganizer.update_movie_file_name_thread import UpdateMovieFileNameThread


class Model(qtc.QObject):

    thread_pool = qtc.QThreadPool()

    analyzation_of_media_folder_complete_signal = qtc.Signal(object)
    error_message_signal = qtc.Signal(str)
    status_update_signal = qtc.Signal(int, str)
    update_file_names_complete_signal = qtc.Signal(str)

    def update_file_names(self, media_file_list, directory):
        """
        Starts the appropriate thread based on if the media is a movie or TV show to update the file(s) names.

        :param media_file_list: A list of file(s) that need their file name changed.
        :param directory: Location of where the file(s) are located.
        :return:
        """
        if 'movies' in directory.lower():
            update_movie_file_name_thread = UpdateMovieFileNameThread(media_file_list, directory)
            update_movie_file_name_thread.signals.progress.connect(self.status_update)
            update_movie_file_name_thread.signals.finish.connect(self.complete_update_file_names)
            self.thread_pool.start(update_movie_file_name_thread)
        else:   # TV show thread
            update_tv_show_file_names_thread = UpdateTvShowFileNamesThread(media_file_list, directory)
            update_tv_show_file_names_thread.signals.progress.connect(self.status_update)
            update_tv_show_file_names_thread.signals.finish.connect(self.complete_update_file_names)
            self.thread_pool.start(update_tv_show_file_names_thread)

    @qtc.Slot(str)
    def complete_update_file_names(self, completed_message):
        """
        Signal for completion of either UpdateTvShowFileNamesThread or UpdateMovieFileNameThread

        :return:
        """
        self.update_file_names_complete_signal.emit(completed_message)

    @qtc.Slot(int, str)
    def status_update(self, progress_bar_percentage, status_message):
        """
        Update the progress bar and status message on screen.

        :param progress_bar_percentage: The int value for the progress bar
        :param status_message: Message to display on the status bar
        :return:
        """
        self.status_update_signal.emit(progress_bar_percentage, status_message)

    @qtc.Slot(str)
    def analyze_media_folder(self, directory):
        """
        Checks the directory to see if it's a media folder for a movie or TV show. If it passes: creates a list of the
        media file(s) in the directory given; and determines if the directory is for a movie or TV show,
        the tile of the show and if a TV show the TV show's season number.

        :param directory: Location of the media file(s)
        :return: a tuple with the following information (list of media file(s), media type, title of show)
        """
        # TODO Check to see if files are already been updated to match show name. If so, inform user.
        media_file_list = []

        # determine if directory is a media folder
        if any(i in directory.lower() for i in ['movies', 'tv shows']):

            # create a list of the media files in directory
            for item in os.listdir(directory):
                if any(item.endswith(extension) for extension in ['.mkv', '.mp4', '.avi']):
                    media_file_list.append(item)

            if media_file_list:
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
            else:
                self.error_message_signal.emit('No media was found in folder: ' + directory)

        else:
            self.error_message_signal.emit('Folder selected is not a media folder. ' + directory)
