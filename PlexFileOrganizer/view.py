from .classes import GenerateMediaFolder
from PySide6 import (
    QtWidgets as qtw,
    QtCore as qtc
)
from .pop_up_windows import (
    MediaFileSelect,
    CreateMediaFolder,
    AutoUpdateMediaFilesWindow,
    ModifiedMediaFolderWindow
)

class View(qtw.QWidget):
    """The front-end of the program"""

    signal_initiate_creating_media_folder = qtc.Signal(object)
    signal_initiate_auto_update_media_files = qtc.Signal(object)
    signal_initiate_scan_of_media_folder = qtc.Signal(str)
    signal_initiate_update_of_media_folder = qtc.Signal(object)
    signal_user_confirmation_of_existing_media_folder = qtc.Signal()
    signal_reset_progress_bar = qtc.Signal()

    # Data pass-through to pop-up windows
    data_pass_through_media_folder_scan_result = qtc.Signal(object)

    def __init__(self):
        super().__init__()

        # Variables
        self.generate_media_folder_data_class = GenerateMediaFolder() # TODO have the window create the class versus created here
        self.auto_update_media_files_options = {'directory': '', 'scan_extra_folder': False} # contains information for the AutoUpdateMediaFilesThread

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
        self.btn_quit_app.clicked.connect(qtc.QCoreApplication.instance().quit)

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
    def launch_create_media_folder_window(self):
        """
        Launches the Create Media Folder window.

        :return:
        """
        create_media_folder_window = CreateMediaFolder(self.generate_media_folder_data_class, self)
        create_media_folder_window.accepted.connect(self.initiate_create_media_folder_thread)
        self.log_window.insertPlainText('\nOpening Create Media Folder window')
        create_media_folder_window.exec()

    @qtc.Slot()
    def launch_modified_media_folder_window(self):
        """
        Launches the "Modified Existing Media Folder" window.

        :return:
        """
        modified_media_folder_window = ModifiedMediaFolderWindow(self)
        modified_media_folder_window.signal_initiate_scan_of_media_folder.connect(self.initiate_scan_of_media_folder_thread)
        modified_media_folder_window.signal_reset_progress_bar.connect(self.signal_reset_progress_bar)
        modified_media_folder_window.signal_media_folder_update_information.connect(self.initiate_update_of_media_folder_thread)
        self.data_pass_through_media_folder_scan_result.connect(modified_media_folder_window.load_existing_media_folder_info)
        self.log_window.insertPlainText('\nOpening "Modified Existing Media Folder" window')
        modified_media_folder_window.exec()

    @qtc.Slot()
    def launch_auto_update_media_files_conformation_window(self):
        """
        Launches pop-up window Auto-Update Media Files Confirmation.

        :return:
        """
        auto_update_media_files_conformation_window = AutoUpdateMediaFilesWindow(self.auto_update_media_files_options, self)
        auto_update_media_files_conformation_window.accepted.connect(self.initiate_auto_update_media_files_thread)
        self.log_window.insertPlainText('\nOpening "Auto-Update Media Files Conformation" window')
        auto_update_media_files_conformation_window.exec()

    @qtc.Slot()
    def launch_manual_update_media_files_window(self):
        """
        Launches the Manual Update Media Files window.

        :return:
        """
        response = qtw.QMessageBox.information(
            self,
            'Feature coming in V1.0.0!',
            'The feature to manual rename media files will be coming in version 1.0.0.'
        )
        if response == qtw.QMessageBox.Ok:
            self.log_window.insertPlainText('\nFeature "Manual Update Media Files" coming soon')

# *** Methods that start threads ***
    @qtc.Slot()
    def initiate_create_media_folder_thread(self):
        """
        The view-side to initiates the process to launch the thread to create the media folder.

        :return:
        """
        self.signal_initiate_creating_media_folder.emit(self.generate_media_folder_data_class)

    @qtc.Slot()
    def initiate_auto_update_media_files_thread(self):
        """
        The view-side to initiate the process to launch thread to start
        auto-update media files.

        :return:
        """
        self.signal_initiate_auto_update_media_files.emit(self.auto_update_media_files_options)

    @qtc.Slot(str)
    def initiate_scan_of_media_folder_thread(self, media_folder_directory):
        """
        The view-side to initiate the process to scan the media folder.

        :param media_folder_directory: the folder location of the media folder to scan.
        :return:
        """
        self.signal_initiate_scan_of_media_folder.emit(media_folder_directory)

    @qtc.Slot(object)
    def initiate_update_of_media_folder_thread(self, media_folder_info):
        """
        The view-side to initiate the process to update the media folder.

        :param media_folder_info: the information of the media folder to update.
        """
        self.signal_initiate_update_of_media_folder.emit(media_folder_info)

# *** Methods that launches messageboxes ***
    @qtc.Slot()
    def messagebox_inform_user_of_existing_media_file(self):
        response = qtw.QMessageBox.information(
            self,
            'Media Folder Already Exists',
            'The Media Folder you wish to make already exists. Please click "ok" to cancel creation of Media Folder.'
        )

        if response == qtw.QMessageBox.Ok:
            self.signal_user_confirmation_of_existing_media_folder.emit()

    @qtc.Slot()
    def messagebox_auto_update_media_files_complete(self):
        """
        Launches the messagebox to inform user the auto update media file(s) is complete.
        And reset the progress bar once user closes the window

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
    def messagebox_create_media_folder_complete(self):
        """
        Launches the messagebox to inform user the creation of the media folder is complete,
        and reset the progress bar once user closes the window.
        """
        response = qtw.QMessageBox.information(
            self,
            'Create Media Folder Complete!',
            'Finished creating the media folder in the directory.'
        )

        if response == qtw.QMessageBox.Ok:
            self.signal_reset_progress_bar.emit()

    @qtc.Slot()
    def messagebox_inform_user_of_folder_not_media_folder(self):
        """
        Launches the messagebox to inform user the folder is not media folder.
        """
        response = qtw.QMessageBox.information(
            self,
            'Selected Folder is not Media Folder!',
            'The folder you selected to analyze is not a Media Folder.'
        )
        if response == qtw.QMessageBox.Ok:
            self.signal_reset_progress_bar.emit()

    @qtc.Slot()
    def messagebox_update_of_media_folder_complete(self):
        """
        Launches a messagebox to inform user the update of the media folder is complete,
        and reset the progress bar once user closes the window.
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
    def clear_log_window(self):
        """
        Clear the list, reset media_label and show_title_label, and disable buttons.

        :return:
        """
        self.log_window.clear()
        self.log_window.insertPlainText('Media Log Window')

    @qtc.Slot(str)
    def write_to_log_window(self, message):
        """
        Writes into the Media Log Window.

        :param message: message to display to user
        :return:
        """
        self.log_window.insertPlainText('\n' + message)
