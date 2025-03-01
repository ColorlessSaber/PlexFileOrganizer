"""
The back-end of the Plex File Organizer
"""
import os
from PySide6 import QtCore as qtc
from PlexFileOrganizer.threads import ScanDirectoryThread, CreateMediaFolderThread


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
    def start_scan_of_directory_thread(self, directory_path, current_media_file_list, files_in_extra_folders_are_formated):
        """
        Starts the thread to scan the selected directory.

        :param directory_path: The directory path the user wishes to scan
        :param current_media_file_list: The media files that were found in the previous directory scan
        :param files_in_extra_folders_are_formated: a flag that makes the function define all files in extra folders are
        formated correctly or not. True - formated correctly, False - not formated correctly.
        :return:
        """
        scan_directory_thread = ScanDirectoryThread(directory_path, current_media_file_list,
                                                    files_in_extra_folders_are_formated)
        scan_directory_thread.signals.progress.connect(self.update_progress_signal)
        self.thread_pool.start(scan_directory_thread)

    @qtc.Slot(str)
    def complete_update_file_names(self, completed_message):
        """
        Signal for completion of either UpdateTvShowFileNamesThread or UpdateMovieFileNameThread

        :return:
        """
        self.update_file_names_complete_signal.emit(completed_message)
