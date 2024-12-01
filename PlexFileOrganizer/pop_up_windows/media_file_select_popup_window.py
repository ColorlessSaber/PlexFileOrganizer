"""
Pop-up window to allow user to select media files they wish to update.
"""
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

class MediaFileSelect(qtw.QDialog):

    def __init__(self, parent=None):
        # The modal=True makes sure the user cannot click the main screen until they close the popup
        super().__init__(parent, modal=True)
        self.setWindowTitle("Media File Select")

        # widgets
        self.add_files_btn = qtw.QPushButton('Add File(s)', self)
        self.remove_file_btn = qtw.QPushButton('Remove File(s)', self)
        self.update_files_btn = qtw.QPushButton('Update File(s)', self)
        self.cancel_btn = qtw.QPushButton('Cancel', self)
        self.cancel_btn.clicked.connect(self.close)

        # layout
        self.setLayout(qtw.QVBoxLayout())
        self.layout().addWidget(self.add_files_btn)
        self.layout().addWidget(self.remove_file_btn)
        self.layout().addWidget(self.update_files_btn)
        self.layout().addWidget(self.cancel_btn)
