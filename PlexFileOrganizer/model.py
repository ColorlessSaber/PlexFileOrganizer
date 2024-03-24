"""
The back-end of the Plex File Organizer
"""
import os
from PySide6 import QtCore as qtc
from PlexFileOrganizer.update_file_names_thread import UpdateFileNamesThread


class Model(qtc.QObject):

    create_list_of_media_files_complete_signal = qtc.Signal(object)
    status_update_signal = qtc.Signal(int, str)
    update_file_names_complete_signal = qtc.Signal(int, str)

    def update_file_names(self, file_list, location):
        """
        Starts the thread to update the file(s) names.

        :param file_list: A list of file(s) with their old name to their new name.
        :param location: Location of where the file(s) are located.
        :return:
        """
        update_file_names_thread = UpdateFileNamesThread(file_list, location)
        update_file_names_thread.signals.progress(self.status_update)
        update_file_names_thread.signals.finish(self.complete_update_file_names)

    def complete_update_file_names(self):
        """
        Signal for completion of the UpdateFileNamesThread

        :return:
        """
        self.update_file_names_complete_signal.emit(100, 'Update File Names Complete')

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
    def create_list_of_media_files(self, directory):
        """
        Creates a list of the media file(s) in the directory given

        :param directory: Location of the media file(s)
        :return:
        """
        media_file_list = []

        # create a list of the media files in directory
        for item in os.listdir(directory):
            if any(item.endswith(extension) for extension in ['.mkv', '.mp4', '.avi']):
                media_file_list.append(item)

        self.create_list_of_media_files_complete_signal.emit(media_file_list)
