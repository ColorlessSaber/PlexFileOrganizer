from PySide6 import (
    QtWidgets as qtw,
    QtCore as qtc
)
from .pop_up_windows import (
    ManualMediaFileUpdate,
    CreateMediaFolder,
    AutoUpdateMediaFilesWindow,
    ModifiedMediaFolderWindow
)

class View(qtw.QWidget):
    """The front-end of the program"""

    # Signal(s) that connect to the model
    signal_initiate_creating_media_folder = qtc.Signal(object)
    signal_initiate_auto_update_media_files = qtc.Signal(dict)
    signal_initiate_scan_of_media_folder = qtc.Signal(str)
    signal_initiate_update_of_media_folder = qtc.Signal(object)
    signal_initiate_manual_update = qtc.Signal(list)
    signal_check_list_of_files_for_duplicates = qtc.Signal(list)
    signal_user_confirmation_of_existing_media_folder = qtc.Signal()

    # Signal(s) that connect to the main_window
    signal_reset_progress_bar = qtc.Signal()
    signal_close_application = qtc.Signal()

    # Data pass-through to pop-up window(s)
    data_pass_through_media_folder_scan_result = qtc.Signal(object)
    data_pass_through_duplicate_check_result = qtc.Signal(list)

    # status pass-through to pop-up window(s)
    status_pass_through_manual_update_media_files_complete = qtc.Signal()
    status_pass_through_media_folder_already_exists = qtc.Signal()
    status_pass_through_media_folder_creation_complete = qtc.Signal()

    def __init__(self):
        super().__init__()

        # widgets
        self.btn_create_media_folder = qtw.QPushButton('Create Media Folder', self)
        self.btn_create_media_folder.clicked.connect(self.launch_create_media_folder_window)

        self.btn_modified_existing_media_folder = qtw.QPushButton('Modified Existing Media Folder', self)
        self.btn_modified_existing_media_folder.clicked.connect(self.launch_modified_media_folder_window)

        self.btn_auto_update_media_files = qtw.QPushButton('Auto-Update Media Files', self)
        self.btn_auto_update_media_files.clicked.connect(self.launch_auto_update_media_files_conformation_window)

        self.btn_manual_update_media_files = qtw.QPushButton('Manual-Update Media Files', self)
        self.btn_manual_update_media_files.clicked.connect(self.launch_manual_update_media_files_window)

        self.btn_clear_log = qtw.QPushButton('Clear Log', self)
        self.btn_clear_log.clicked.connect(self.clear_log_window)

        self.btn_quit_app = qtw.QPushButton('Quit Application', self)
        self.btn_quit_app.clicked.connect(self.signal_close_application)

        self.log_window = qtw.QTextBrowser()
        self.log_window.insertPlainText('Media Log Window')

        # Set up the layout of window
        # QGridLayout placement order: row, column, row-span, column-span
        grid_layout = qtw.QGridLayout()
        grid_layout.addWidget(self.btn_create_media_folder, 0, 0)
        grid_layout.addWidget(self.btn_auto_update_media_files, 0, 1)
        grid_layout.addWidget(self.btn_manual_update_media_files, 0, 2)
        grid_layout.addWidget(self.btn_modified_existing_media_folder, 1, 0)
        grid_layout.addWidget(self.log_window, 3, 0, 5, 4)
        grid_layout.addWidget(self.btn_clear_log, 8, 0)
        grid_layout.addWidget(self.btn_quit_app, 8, 3)
        self.setLayout(grid_layout)

# *** Methods that launch popup windows ***
    @qtc.Slot()
    def launch_create_media_folder_window(self) -> None:
        """
        Launches the Create Media Folder window.

        :return:
        """
        create_media_folder_window = CreateMediaFolder(self)
        create_media_folder_window.signal_initiate_create_media_folder.connect(self.signal_initiate_creating_media_folder)
        create_media_folder_window.signal_reset_progress_bar.connect(self.signal_reset_progress_bar)
        self.status_pass_through_media_folder_already_exists.connect(create_media_folder_window.messagebox_media_folder_already_exists)
        self.status_pass_through_media_folder_creation_complete.connect(create_media_folder_window.messagebox_media_folder_creation_complete)
        self.log_window.insertPlainText('\nOpening Create Media Folder window')
        create_media_folder_window.exec()

    @qtc.Slot()
    def launch_modified_media_folder_window(self) -> None:
        """
        Launches the "Modified Existing Media Folder" window.

        :return:
        """
        modified_media_folder_window = ModifiedMediaFolderWindow(self)
        modified_media_folder_window.signal_initiate_scan_of_media_folder.connect(self.signal_initiate_scan_of_media_folder)
        modified_media_folder_window.signal_reset_progress_bar.connect(self.signal_reset_progress_bar)
        modified_media_folder_window.signal_media_folder_update_information.connect(self.signal_initiate_update_of_media_folder)
        self.data_pass_through_media_folder_scan_result.connect(modified_media_folder_window.load_existing_media_folder_info)
        self.log_window.insertPlainText('\nOpening "Modified Existing Media Folder" window')
        modified_media_folder_window.exec()

    @qtc.Slot()
    def launch_auto_update_media_files_conformation_window(self) -> None:
        """
        Launches pop-up window Auto-Update Media Files Confirmation.

        :return:
        """
        auto_update_media_files_conformation_window = AutoUpdateMediaFilesWindow(self)
        auto_update_media_files_conformation_window.signal_initiate_auto_update.connect(self.signal_initiate_auto_update_media_files)
        self.log_window.insertPlainText('\nOpening "Auto-Update Media Files Conformation" window')
        auto_update_media_files_conformation_window.exec()

    @qtc.Slot()
    def launch_manual_update_media_files_window(self) -> None:
        """
        Launches the Manual Update Media Files window.

        :return:
        """
        manual_update_media_files_window = ManualMediaFileUpdate(self)
        self.data_pass_through_duplicate_check_result.connect(manual_update_media_files_window.second_stage_update_process)
        self.status_pass_through_manual_update_media_files_complete.connect(manual_update_media_files_window.messagebox_manual_update_media_files_complete)
        manual_update_media_files_window.signal_initiate_manual_update.connect(self.signal_initiate_manual_update)
        manual_update_media_files_window.signal_check_list_of_files_for_duplicates.connect(self.signal_check_list_of_files_for_duplicates)
        manual_update_media_files_window.signal_reset_progress_bar.connect(self.signal_reset_progress_bar)
        self.log_window.insertPlainText('\nOpening Manual Update Media Files window')
        manual_update_media_files_window.exec()

# *** Methods that launches messageboxes ***
    @qtc.Slot()
    def messagebox_auto_update_media_files_complete(self) -> None:
        """
        Launches the messagebox to inform user the auto update media file(s) is complete.
        Will reset the progress bar once user closes the messagebox window.

        :return:
        """
        response = qtw.QMessageBox.information(
            self,
            'Auto Update Media Files Complete!',
            'Finished scanning the selected directory. Please see console window for information on if any files were updated during the scan.'
        )

        if response == qtw.QMessageBox.Ok:
            self.signal_reset_progress_bar.emit()

    @qtc.Slot()
    def messagebox_inform_user_of_folder_not_media_folder(self) -> None:
        """
        Launches the messagebox to inform user the folder is not media folder.
        Will reset the progress bar once user closes the messagebox window.

        :return:
        """
        response = qtw.QMessageBox.information(
            self,
            'Selected Folder is not Media Folder!',
            'The folder you selected to analyze is not a Media Folder.'
        )
        if response == qtw.QMessageBox.Ok:
            self.signal_reset_progress_bar.emit()

    @qtc.Slot()
    def messagebox_update_of_media_folder_complete(self) -> None:
        """
        Launches a messagebox to inform user the update of the media folder is complete,
        and reset the progress bar once user closes the window.

        :return:
        """
        response = qtw.QMessageBox.information(
            self,
            'Update Media Folder Complete!',
            'Finished updating the media folder in the directory.'
        )

        if response == qtw.QMessageBox.Ok:
            self.signal_reset_progress_bar.emit()

# *** Methods for Log Window ***
    @qtc.Slot()
    def clear_log_window(self) -> None:
        """
        Clear the list, reset media_label and show_title_label, and disable buttons.

        :return:
        """
        self.log_window.clear()
        self.log_window.insertPlainText('Media Log Window')

    @qtc.Slot(str)
    def write_to_log_window(self, message: str) -> None:
        """
        Writes into the Media Log Window.

        :param message: message to display to user
        :return:
        """
        self.log_window.insertPlainText('\n' + message)
