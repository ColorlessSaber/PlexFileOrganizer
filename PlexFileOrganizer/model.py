from PySide6 import QtCore as qtc
from PlexFileOrganizer.threads import CreateMediaFolderThread, AutoUpdateMediaFilesThread


class Model(qtc.QObject):
    """The back-end of the Plex File Organizer"""

    thread_pool = qtc.QThreadPool()

    signal_user_input_request = qtc.Signal()
    signal_user_input_response = qtc.Signal()
    signal_error_message = qtc.Signal(object)
    signal_update_progress = qtc.Signal(int, str)
    signal_finished = qtc.Signal(str)
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
        create_media_folder_thread.signals.request_user_input_signal.connect(self.signal_user_input_request) #TODO make this connect to a model method
        create_media_folder_thread.signals.progress.connect(self.slot_thread_update_progress_status)
        #TODO add in signal to launch popup to inform user the task is done.
        self.signal_user_input_response.connect(create_media_folder_thread.user_confirmation) #TODO make this connect to a model method
        self.thread_pool.start(create_media_folder_thread)

    @qtc.Slot(object)
    def start_auto_update_media_files_thread(self, user_selected_options):
        """
        Creates and starts the thread to Auto Update Media Files.

        :param user_selected_options: The directory that contains the directory user selected, and
        other selectable options.
        :return:
        """
        auto_update_media_files_threads = AutoUpdateMediaFilesThread(user_selected_options)
        auto_update_media_files_threads.signals.progress.connect(self.slot_thread_update_progress_status)
        auto_update_media_files_threads.signals.error.connect(self.slot_thread_error_message)
        auto_update_media_files_threads.signals.finished.connect(self.slot_thread_finished)
        self.thread_pool.start(auto_update_media_files_threads)

# *** Signals to inform or request input from user methods ***
    @qtc.Slot(int, str)
    def slot_thread_update_progress_status(self, progress_bar_percentage, message):
        """
        The slot on the model side for all threads' signals.progress to connect to for sending out a progress update--change to progress
        bar and message to print to user.

        :param progress_bar_percentage: An int value to set the progress bar position.
        :param message: A string message to be printed out to the user.
        :return:
        """
        self.signal_update_progress.emit(progress_bar_percentage, message)

    @qtc.Slot(str)
    def slot_thread_finished(self, completed_task):
        """
        The slot on the model side for all threads' signals.finished to connect to for commanding the view
        what messagebox to display to inform user the task is completed

        :param completed_task: The task that was completed, string form
        :return:
        """
        self.signal_finished.emit(completed_task)

    @qtc.Slot(object)
    def slot_thread_error_message(self, error_message):
        """
        The slot on the model side for all threads' signals.error to connect to for sending out an error message
        to the user.

        :param error_message: The string error message to be printed out to the user.
        :return:
        """
        #print(error_message) # for debugging
        self.signal_error_message.emit(error_message)
