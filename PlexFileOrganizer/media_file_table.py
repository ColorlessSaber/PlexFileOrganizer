from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

class MediaFileTable(qtc.QAbstractTableModel):
    """A table to allow user to view and modify what the file's new name should be"""

    def __init__(self, current_media_file_list):
        super().__init__()

        self.current_media_file_list = current_media_file_list
        self._headers = ['Current File Name', 'New File Name']

    def rowCount(self, /, parent= ...):
        return len(self.current_media_file_list)

    def columnCount(self, /, parent= ...):
        return len(self._headers)
