"""
The front-end of the program
"""
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PlexFileOrganizer.pop_up_windows import MediaFileSelect, CreateMediaFolders

class View(qtw.QWidget):
    start_creating_media_folders_signal = qtc.Signal(dict)

    def __init__(self):
        super().__init__()

        # Variables
        self.create_media_folders_selection = {
            'directory': None,
            'movie or tv': None,
            'media title': None,
            'season num': None,
            'extra folders': {
                'trailer': False,
                'behind the scenes': False,
                'deleted scenes': False,
                'featurettes': False,
                'interviews': False,
                'scenes': False,
                'shorts': False,
                'other': False
            }
        }

        # pop-up windows
        self.create_media_folders_window = None
        self.select_media_files_window = None

        # widgets
        self.update_media_files_btn = qtw.QPushButton('Update Media Files', self)
        self.update_media_files_btn.clicked.connect(self.update_media_files)

        self.create_media_folders_btn = qtw.QPushButton('Create Media Folder(s)', self)
        self.create_media_folders_btn.clicked.connect(self.create_media_folders)

        self.clear_log_btn = qtw.QPushButton('Clear Log', self)
        self.clear_log_btn.clicked.connect(self.clear_log_window)

        self.quit_app_btn = qtw.QPushButton('Quiet Application', self)
        self.quit_app_btn.clicked.connect(qtc.QCoreApplication.instance().quit)

        self.log_window = qtw.QTextBrowser()
        self.log_window.insertPlainText('Media Log Window')

        # layout
        grid_layout = qtw.QGridLayout()
        grid_layout.addWidget(self.update_media_files_btn, 0, 0)
        grid_layout.addWidget(self.create_media_folders_btn, 0, 1)
        grid_layout.addWidget(self.log_window, 2, 0, 5, 4)
        grid_layout.addWidget(self.clear_log_btn, 7, 0)
        grid_layout.addWidget(self.quit_app_btn, 7, 3)
        self.setLayout(grid_layout)


    @qtc.Slot()
    def create_media_folders(self):
        """
        Launches pop-up window to allow user to select folder(s) to create

        :return:
        """
        self.log_window.insertPlainText('\nOpening Create Media Folder(s) Window')
        self.create_media_folders_window = CreateMediaFolders(self.create_media_folders_selection, self)
        self.create_media_folders_window.accepted.connect(self.start_create_media_folders_thread)
        self.create_media_folders_window.exec()

    @qtc.Slot()
    def start_create_media_folders_thread(self):
        """
        Starts the thread to create the media folder(s).

        :return:
        """
        self.start_creating_media_folders_signal.emit(self.create_media_folders_selection)

    @qtc.Slot()
    def update_media_files(self):
        """
        Launches pop-up window to allow user to select media file(s) that need to be updated

        :return:
        """
        self.log_window.insertPlainText('\nOpening Media File Select Window')
        self.select_media_files_window = MediaFileSelect(self)
        self.select_media_files_window.exec()

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
