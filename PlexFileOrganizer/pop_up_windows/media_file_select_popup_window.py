"""
Pop-up window to allow user to select media files they wish to update.
"""
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

class MediaFileSelect(qtw.QDialog):
    start_scan_of_directory_signal = qtc.Signal(str, object, bool)


    def __init__(self, parent=None):
        # The modal=True makes sure the user cannot click the main screen until they close the popup
        super().__init__(parent, modal=True)
        self.setWindowTitle("Media File Select")

        # variables
        self.current_media_file_list = []
        self.files_in_extra_folders_are_formated = True

        # widgets
        self.scan_folder_btn = qtw.QPushButton('Scan Folder', self)
        self.scan_folder_btn.clicked.connect(self.select_directory_popup)
        self.add_files_btn = qtw.QPushButton('Add File(s)', self)
        self.remove_file_btn = qtw.QPushButton('Remove File(s)', self)
        self.update_files_btn = qtw.QPushButton('Update File(s)', self)
        self.cancel_btn = qtw.QPushButton('Cancel', self)
        self.cancel_btn.clicked.connect(self.close)

        # layout
        self.setLayout(qtw.QVBoxLayout())
        self.layout().addWidget(self.scan_folder_btn)
        self.layout().addWidget(self.add_files_btn)
        self.layout().addWidget(self.remove_file_btn)
        self.layout().addWidget(self.update_files_btn)
        self.layout().addWidget(self.cancel_btn)

    @qtc.Slot()
    def select_directory_popup(self):
        directory = qtw.QFileDialog.getExistingDirectory(
            self,
            'Select folder...',
            qtc.QDir.homePath()
        )

        if directory:
            self.start_scan_of_directory_signal.emit(directory,
                                                     self.current_media_file_list,
                                                     self.files_in_extra_folders_are_formated)
