"""
Pop-up window to allow user to select media files they wish to update.
"""
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

class MediaFileSelect(qtw.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(qtc.Qt.WindowStaysOnTopHint)

        # widgets
        self.add_files_btn = qtw.QPushButton('Add File(s)', self)
        self.remove_file_btn = qtw.QPushButton('Remove File(s)', self)
        self.update_files_btn = qtw.QPushButton('Update File(s)', self)
        self.cancel_btn = qtw.QPushButton('Cancel', self)
        self.cancel_btn.clicked.connect(self.close())

        # layout
        self.setLayout(qtw.QVBoxLayout())
        self.layout().addWidget(self.add_files_btn)
        self.layout().addWidget(self.remove_file_btn)
        self.layout().addWidget(self.update_files_btn)
        self.layout().addWidget(self.cancel_btn)
