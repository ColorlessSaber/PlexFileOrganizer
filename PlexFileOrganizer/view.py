"""
The front-end of the program
"""
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc


class View(qtw.QWidget):
    start_analyzing_media_folder_signal = qtc.Signal(str)
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

        self.media_label = qtw.QLabel('Media: ')    # if the media is a movie or TV show
        self.show_title_label = qtw.QLabel('Show Title: ')  # title of the media; and if TV show, the season as well.

        self.update_files_btn = qtw.QPushButton('Update File(s)', self)
        self.clear_list_btn = qtw.QPushButton('Clear List', self)
        self.clear_list_btn.clicked.connect(self.clear_screen)

        self.quit_app_btn = qtw.QPushButton('Quiet Application', self)
        self.quit_app_btn.clicked.connect(qtc.QCoreApplication.instance().quit)

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

        if directory:
            self.media_files_directory = directory
            self.start_analyzing_media_folder_signal.emit(directory)

    @qtc.Slot(object)
    def update_media_information_view(self, media_information):
        """
        Clear and update the media_list_view widget and save the list to a variable; and update the labels on screen
        to inform user what the media type they have selected, the tile of the show and if a TV show the TV show's
        season number.

        :param media_information: A tuple with the following information (list of media file(s), media type,
        title of media)
        :return:
        """
        self.media_files_list = media_information[0]
        self.media_label.setText('Media: ' + media_information[1])
        self.show_title_label.setText('Show Title: ' + media_information[2])
        self.media_list_view.clear()
        self.media_list_view.addItems(media_information[0])

    @qtc.Slot()
    def clear_screen(self):
        """
        Clear the list, and reset media_label and show_title_label.

        :return:
        """
        self.media_list_view.clear()
        self.media_label.setText('Media: ')
        self.show_title_label.setText('Title: ')

    @qtc.Slot(str)
    def error_message_popup(self, error_message):
        """
        Display an error message to the user.

        :param error_message:
        :return:
        """
        qtw.QMessageBox.critical(
            self,
            'Error Message!',
            'The program ran into the following problem: ' + error_message
        )
