"""
The front-end of the program
"""
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc


class View(qtw.QWidget):
    start_analyzing_media_folder_signal = qtc.Signal(str)
    start_update_file_names_thread_signal = qtc.Signal(list, str)

    def __init__(self):
        super().__init__()

        # widgets
        self.update_media_files_btn = qtw.QPushButton('Update Media Files', self)
        self.create_media_folders_btn = qtw.QPushButton('Create Media Folder(s)', self)

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

        # variables
        self.media_files_directory = ''
        self.media_files_list = []

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

    @qtc.Slot()
    def clear_log_window(self):
        """
        Clear the list, reset media_label and show_title_label, and disable buttons.

        :return:
        """
        self.log_window.clear()
        self.log_window.insertPlainText('Media Log Window')

    @qtc.Slot(str)
    def completed_message_popup(self, completed_message):
        """
        Writes into the Media Log Window that the task is completed.

        :param completed_message: message to display to user
        :return:
        """
        self.log_window.insertPlainText('\n'+completed_message)

    @qtc.Slot(str)
    def error_message_popup(self, error_message):
        """
        Writes into the Media Log Window the error that was ran into while trying to complete the task.

        :param error_message:
        :return:
        """
        self.log_window.insertPlainText('\n'+error_message)
