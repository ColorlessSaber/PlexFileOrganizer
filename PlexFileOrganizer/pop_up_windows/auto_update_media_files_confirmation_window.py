"""
Pop-up window to warn user how the Auto-Update Media Files process work,
and get final confirmation that they wish to process, along with input if to update the files in
the extra folders as well
"""
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtCore as qtc

class AutoUpdateMediaFilesWindow(qtw.QDialog):

    def __init__(self, user_selected_dir_and_options, parent=None):
        """

        :param user_selected_dir_and_options: A dictionary containing the directory the user has selected,
        and if they wish to update the media files in the extra folder(s).
        :param parent: The parent window the dialog window will be linked to.
        """
        # The modal=True makes sure the user cannot click the main screen until they close the popup
        super().__init__(parent, modal=True)
        self.setWindowTitle('Auto-Update Media Files Confirmation')

        self.user_selected_dir_and_options = user_selected_dir_and_options

        # Labels
        label_information_of_process = qtw.QLabel(
            """
            The Auto-Update Media Files process will automatically scan the selected media folder below.\n
            This process will auto-number tv shows as they are alphabetically ordered in the folder they are in.\n
            If you know the media files aren't in the correct order, then cancel the process and\n
            use the "Manual Update Media Files" option on
            main window.
            """,
            self
        )
        label_information_of_process.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.label_selected_directory = qtw.QLabel('', self)

        # buttons and checkbox creation
        self.cb_extra_folders_to_be_scanned = qtw.QCheckBox('Update media files in Extra Folder(s)', self)
        self.btn_select_directory = qtw.QPushButton('Select Directory', self)
        self.btn_select_directory.clicked.connect(self.select_directory_window)
        self.btn_proceed = qtw.QPushButton('Proceed', self)
        self.btn_proceed.setEnabled(False)
        self.btn_proceed.clicked.connect(self.accept)
        self.btn_cancel = qtw.QPushButton('Cancel', self)
        self.btn_cancel.clicked.connect(self.reject)

        # Set up the layout of window
        directory_selected_layout = qtw.QHBoxLayout()
        directory_selected_layout.addWidget(self.btn_select_directory)
        directory_selected_layout.addWidget(self.label_selected_directory)

        proceed_cancel_button_layout = qtw.QHBoxLayout()
        proceed_cancel_button_layout.addWidget(self.btn_proceed)
        proceed_cancel_button_layout.addWidget(self.btn_cancel)

        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(label_information_of_process)
        main_layout.addLayout(directory_selected_layout)
        main_layout.addWidget(self.cb_extra_folders_to_be_scanned)
        main_layout.addLayout(proceed_cancel_button_layout)
        self.setLayout(main_layout)

    @qtc.Slot()
    def select_directory_window(self):
        """
        Open a directory selector window

        :return:
        """
        directory_selected_by_user = qtw.QFileDialog.getExistingDirectory(
            self,
            'Select folder...',
            qtc.QDir.homePath()
        )

        # confirm user selected a directory
        if directory_selected_by_user:
            self.btn_proceed.setEnabled(True) # enable the button given user has selected a directory
            self.user_selected_dir_and_options['directory'] = directory_selected_by_user
            self.label_selected_directory.setText(directory_selected_by_user)

    def accept(self):
        """
        Update the auto_update_media_files_options with user's selections before closing window.

        :return:
        """
        self.user_selected_dir_and_options['scan_extra_folder'] = self.cb_extra_folders_to_be_scanned.isChecked()
        super().accept()