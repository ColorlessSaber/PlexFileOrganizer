from PySide6 import QtCore as qtc
from PlexFileOrganizer.threads import ScanDirectoryThread, CreateMediaFolderThread, AutoUpdateMediaFilesThread


class Model(qtc.QObject):
    """The back-end of the Plex File Organizer"""

    thread_pool = qtc.QThreadPool()

    signal_user_input_request = qtc.Signal()
    signal_user_input_response = qtc.Signal()
    signal_error_message = qtc.Signal(str)
    signal_update_progress = qtc.Signal(int, str)
    signal_analysis_of_media_folder_complete = qtc.Signal(object)
    signal_update_file_names_complete = qtc.Signal(str)

# *** The creation and start of thread methods ***
    @qtc.Slot(object)
    def start_create_media_folder_thread(self, media_folder_selection):
        """
        Starts the thread to create the folder(s) the user wishes to make.

        :param media_folder_selection: Dataclass MediaFolder, holding the user inputs and selections.
        :return:
        """
        create_media_folder_thread = CreateMediaFolderThread(media_folder_selection)
        create_media_folder_thread.signals.request_user_input_signal.connect(self.signal_user_input_request)
        create_media_folder_thread.signals.progress.connect(self.signal_update_progress)
        #TODO add in signal to launch popup to inform user the task is done.
        self.signal_user_input_response.connect(create_media_folder_thread.user_confirmation)
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
        scan_directory_thread.signals.progress.connect(self.signal_update_progress)
        self.thread_pool.start(scan_directory_thread)

    @qtc.Slot(object)
    def start_auto_update_media_files_thread(self, user_selected_options):
        """
        Creates and starts the thread to Auto Update Media Files.

        :param user_selected_options: The directory that contains the directory user selected, and
        other selectable options.
        :return:
        """
        auto_update_media_files_threads = AutoUpdateMediaFilesThread(user_selected_options)
        auto_update_media_files_threads.signals.progress.connect(self.signal_update_progress)
        self.thread_pool.start(auto_update_media_files_threads)

# *** Signals to inform or request input from user methods ***
    @qtc.Slot(str)
    def complete_update_file_names(self, completed_message):
        """
        Signal for completion of either UpdateTvShowFileNamesThread or UpdateMovieFileNameThread

        :return:
        """
        self.signal_update_file_names_complete.emit(completed_message)
