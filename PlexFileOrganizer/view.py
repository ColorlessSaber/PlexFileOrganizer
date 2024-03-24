"""
The front-end of the program
"""
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc


class View(qtw.QWidget):
    start_create_list_of_media_files_signal = qtc.Signal(str)
    start_update_file_names_thread = qtc.Signal(list, str)

    def __init__(self):
        super().__init__()

        # variables
        self.media_files_directory = ''
        self.media_files_list = []

        # widgets
        self.media_list_view = qtw.QListWidget()
        self.media_list_view.setFixedSize(qtc.QSize(300, 400))

        self.select_folder_btn = qtw.QPushButton('Select Folder', self)
        self.select_folder_btn.clicked.connect(self.select_folder)

        self.media_label = qtw.QLabel('Media: ')
        self.show_title_label = qtw.QLabel('Show Title: ')

        self.update_files_btn = qtw.QPushButton('Update File(s)', self)
        self.clear_list_btn = qtw.QPushButton('Clear List', self)
        self.clear_list_btn.clicked.connect(self.media_list_view.clear())

        self.quit_app_btn = qtw.QPushButton('Quiet Application', self)

        # create layout
        grid_layout = qtw.QGridLayout()
        grid_layout.addWidget(self.select_folder_btn, 0, 0)
        grid_layout.addWidget(self.media_label, 1, 0)
        grid_layout.addWidget(self.show_title_label, 2, 0)
        grid_layout.addWidget(self.update_files_btn, 3, 0)
        grid_layout.addWidget(self.clear_list_btn, 4, 0)
        grid_layout.addWidget(self.quit_app_btn, 5, 0)
        grid_layout.addWidget(self.media_list_view, 0, 1, 6, 3)
        self.setLayout(grid_layout)

    @qtc.Slot()
    def select_folder(self):
        """
        Opens a QfileDialog to have user select directory of media file(s) they wish to modify

        :return:
        """

        directory = qtw.QFileDialog.getExistingDirectory(
            self,
            "Select Location of Media File(s)...",
            qtc.QDir.homePath()
        )

        # start the process of creating a list of media file(s) in directory
        if directory:
            self.media_files_directory = directory
            self.start_create_list_of_media_files_signal.emit(directory)

    @qtc.Slot(object)
    def update_media_list_view(self, media_files_list):
        """
        Clear and update the media_list_view widget, and save the list to a variable.

        :param media_files_list: The list of media file(s) found in directory.
        :return:
        """
        self.media_files_list = media_files_list

        self.media_list_view.clear()
        self.media_list_view.addItems(media_files_list)
