from PySide6 import QtCore as qtc
from .functions import (
    build_app_directory,
    setup_app_logger,
    setup_app_settings_file,
    load_app_settings,
    save_app_settings,
)
from .threads import (
    CreateMediaFolderThread,
    AutoUpdateMediaFilesThread,
    ScanExistingMediaFolderThread,
    UpdateExistingMediaFolderThread,
    ManualUpdateMediaFilesThread,
)


class Model(qtc.QObject):
    """The back-end of the Plex File Organizer"""

    thread_pool = qtc.QThreadPool().globalInstance()

    # Signal(s) to inform the user of something
    signal_inform_user_media_folder_already_exists = qtc.Signal()
    signal_user_confirmation_of_existing_media_folder = qtc.Signal()
    signal_inform_user_folder_not_media_folder = qtc.Signal()

    # Signal(s) connect to the main_window
    signal_error_message = qtc.Signal()
    signal_update_progress = qtc.Signal(int, str)

    # Signal(s) connect to model
    signal_analysis_of_media_folder_complete = qtc.Signal(object)
    signal_duplicate_files_check_complete = qtc.Signal(bool)
    signal_auto_update_finished = qtc.Signal()
    signal_create_media_folder_finished = qtc.Signal()
    signal_update_of_media_folder_finished = qtc.Signal()
    signal_manual_update_finished = qtc.Signal()

    def __init__(self):
        super().__init__()
        self.__app_settings_data = {}

    # *** Methods that access Model or application files ***
    @property
    def preferences_data(self):
        return self.__app_settings_data.get("preferences")

    @qtc.Slot()
    def build_application_directory_and_setup_logger(self) -> None:
        """
        Builds the application directory and sets up the logger for the application.

        :return:
        """
        build_app_directory()
        setup_app_logger()
        setup_app_settings_file()
        self.__app_settings_data = load_app_settings()

    # *** Quick methods that don't require threads ***
    @qtc.Slot(list)
    def check_for_duplicates_in_media_file_list(self, media_file_list: list) -> None:
        """
        Checks the list of media files and see if there are duplicates rename file names.
        """
        # pull out all the rename file names from the list
        rename_file_list = [i[2] for i in media_file_list]

        # if the list and set lengths match, then there are no duplicate rename file names.
        if len(rename_file_list) == len(set(rename_file_list)):
            self.signal_duplicate_files_check_complete.emit(True)
        else:
            self.signal_duplicate_files_check_complete.emit(False)
    @qtc.Slot(dict)
    def save_new_app_preferences_to_json_file(self, new_pref_settings: dict) -> None:
        """
        Saves the new preferences to a json file that is located in the application directory.
        :param new_pref_settings: The new preferences settings to save.
        :return:
        """
        self.__app_settings_data["preferences"] = new_pref_settings
        save_app_settings(self.__app_settings_data)

    # *** Methods that create and start a thread ***
    @qtc.Slot(object)
    def start_create_media_folder_thread(self, media_folder_selection: object) -> None:
        """
        Starts the thread to create the folder(s) the user wishes to make.

        :param media_folder_selection: A class holding information of the user's inputs and selections for the new media folder.
        :return:
        """
        create_media_folder_thread = CreateMediaFolderThread(media_folder_selection)
        create_media_folder_thread.signals.media_folder_already_exists.connect(
            self.signal_inform_user_media_folder_already_exists
        )
        create_media_folder_thread.signals.progress.connect(
            self.signal_update_progress
        )
        create_media_folder_thread.signals.error.connect(
            self.signal_error_message
        )
        create_media_folder_thread.signals.finished.connect(
            self.signal_create_media_folder_finished
        )
        self.thread_pool.start(create_media_folder_thread)

    @qtc.Slot(object)
    def start_auto_update_media_files_thread(self, user_selected_options: dict) -> None:
        """
        Creates and starts the thread to Auto Update Media Files.

        :param user_selected_options: The directory that contains the directory user selected, and
        other selectable options.
        :return:
        """
        auto_update_media_files_threads = AutoUpdateMediaFilesThread(
            user_selected_options
        )
        auto_update_media_files_threads.signals.progress.connect(
            self.signal_update_progress
        )
        auto_update_media_files_threads.signals.error.connect(
            self.signal_error_message
        )
        auto_update_media_files_threads.signals.finished.connect(
            self.signal_auto_update_finished
        )
        self.thread_pool.start(auto_update_media_files_threads)

    @qtc.Slot(str)
    def start_scan_of_existing_media_folder_thread(
        self, media_folder_directory: str
    ) -> None:
        """
        Creates and starts the thread to scan an existing media folder.

        :param media_folder_directory: the folder location of the media folder to scan.
        :return:
        """
        scan_existing_media_folder = ScanExistingMediaFolderThread(
            media_folder_directory
        )
        scan_existing_media_folder.signals.progress.connect(
            self.signal_update_progress
        )
        scan_existing_media_folder.signals.error.connect(
            self.signal_error_message
        )
        scan_existing_media_folder.signals.finished.connect(
            self.signal_analysis_of_media_folder_complete
        )
        scan_existing_media_folder.signals.not_media_folder.connect(
            self.signal_inform_user_folder_not_media_folder
        )
        self.thread_pool.start(scan_existing_media_folder)

    @qtc.Slot(object)
    def start_update_of_existing_media_folder_thread(
        self, media_folder_info: object
    ) -> None:
        """
        Creates and starts the thread to update the existing media folder per user's input.

        :param media_folder_info: Information of the existing media folder and what the user wishes to add.
        """
        update_existing_media_folder = UpdateExistingMediaFolderThread(
            media_folder_info
        )
        update_existing_media_folder.signals.progress.connect(
            self.signal_update_progress
        )
        update_existing_media_folder.signals.error.connect(
            self.signal_error_message
        )
        update_existing_media_folder.signals.finished.connect(
            self.signal_update_of_media_folder_finished
        )
        self.thread_pool.start(update_existing_media_folder)

    @qtc.Slot(list)
    def start_manual_update_media_files_thread(self, files_to_update: list) -> None:
        """
        Creates and starts the thread to update the selected media files.

        :param files_to_update: List of media files to update.
        """
        manual_update_media_files_thread = ManualUpdateMediaFilesThread(files_to_update)
        manual_update_media_files_thread.signals.progress.connect(
            self.signal_update_progress
        )
        manual_update_media_files_thread.signals.error.connect(
            self.signal_error_message
        )
        manual_update_media_files_thread.signals.finished.connect(
            self.signal_manual_update_finished
        )
        self.thread_pool.start(manual_update_media_files_thread)
