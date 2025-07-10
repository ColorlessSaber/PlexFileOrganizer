from PlexFileOrganizer.dataclasses import MediaFolder
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PlexFileOrganizer.pop_up_windows import MediaFileSelect, CreateMediaFolder, AutoUpdateMediaFilesWindow

class View(qtw.QWidget):
    """The front-end of the program"""
    initiate_creating_media_folder_signal = qtc.Signal(object)
    initiate_scan_of_directory_signal = qtc.Signal(str, object, bool)
    user_input_response_signal = qtc.Signal()

    def __init__(self):
        super().__init__()

        # Variables
        self.create_media_folder_selection = MediaFolder()
        self.auto_update_media_files_options = {'directory': '', 'scan_extra_folder': False}

        # pop-up windows
        self.create_media_folder_window = None
        self.select_media_files_window = None
        self.auto_update_media_files_conformation_window = None

        # widgets
        self.btn_create_media_folder = qtw.QPushButton('Create Media Folder', self)
        self.btn_create_media_folder.clicked.connect(self.launch_create_media_folder_window)

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
        grid_layout = qtw.QGridLayout()
        grid_layout.addWidget(self.btn_create_media_folder, 0, 0)
        grid_layout.addWidget(self.btn_auto_update_media_files, 0, 1)
        grid_layout.addWidget(self.btn_manual_update_media_files, 0, 2)
        grid_layout.addWidget(self.log_window, 2, 0, 5, 4)
        grid_layout.addWidget(self.btn_clear_log, 7, 0)
        grid_layout.addWidget(self.btn_quit_app, 7, 3)
        self.setLayout(grid_layout)

# *** Methods that launch popup windows ***
    @qtc.Slot()
    def launch_create_media_folder_window(self):
        """
        Launches the Create Media Folder window.

        :return:
        """
        self.log_window.insertPlainText('\nOpening Create Media Folder Window')
        self.create_media_folder_window = CreateMediaFolder(self.create_media_folder_selection, self)
        self.create_media_folder_window.accepted.connect(self.initiate_create_media_folder_thread)
        self.create_media_folder_window.exec()

    @qtc.Slot()
    def launch_auto_update_media_files_conformation_window(self):
        """
        Launches pop-up window Auto-Update Media Files Confirmation.

        :return:
        """
        self.log_window.insertPlainText('\nOpening "Auto-Update Media Files Conformation Window"')
        self.auto_update_media_files_conformation_window = AutoUpdateMediaFilesWindow(self.auto_update_media_files_options, self)
        self.auto_update_media_files_conformation_window.accepted.connect(self.initiate_auto_update_media_files_thread)
        self.auto_update_media_files_conformation_window.exec()

    @qtc.Slot()
    def launch_manual_update_media_files_window(self):
        """
        Launches the Manual Update Media Files window.

        :return:
        """
        self.log_window.insertPlainText('\nOpening "Manual Update Media Files" Window')

# *** Methods that start threads ***
    @qtc.Slot()
    def initiate_create_media_folder_thread(self):
        """
        Initiates the process to launch the thread to create the media folder.

        :return:
        """
        self.initiate_creating_media_folder_signal.emit(self.create_media_folder_selection)

    @qtc.Slot()
    def initiate_auto_update_media_files_thread(self):
        """
        The view-side slot to initiate the process to launch thread to start
        auto-update media files.

        :return:
        """
        print(self.auto_update_media_files_options)

# *** Methods that launches messageboxes ***
    @qtc.Slot()
    def messagebox_inform_user_media_file_exist(self):
        response = qtw.QMessageBox.information(
            self,
            'Media Folder Exists',
            'The Media Folder you wish to make already exists. Please click "ok" to cancel creation of Media Folder.'
        )

        if response == qtw.QMessageBox.Ok:
            self.user_input_response_signal.emit()

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
