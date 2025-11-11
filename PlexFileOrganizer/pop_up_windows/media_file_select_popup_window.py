from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc


class MediaFileTable(qtc.QAbstractTableModel):
    """A table to allow user to view and modify what the file's new name should be"""

    def __init__(self, read_only_indexes, current_media_file_list: list = None, column_names: list = None):
        super().__init__()
        self.read_only_indexes =  read_only_indexes
        self._data = current_media_file_list
        self._headers = column_names

    def rowCount(self, parent=qtc.QModelIndex()) -> int:
        """Return the number of rows in the table"""
        return len(self._data)

    def columnCount(self, parent=qtc.QModelIndex()) -> int:
        """Return the number of columns in the table"""
        return len(self._headers) if self._headers else 0

    def data(self, index, role=qtc.Qt.DisplayRole) -> object | None:
        """Return the data at the given index for display and editing"""
        if not index.isValid():
            return None

        if role in (qtc.Qt.DisplayRole, qtc.Qt.EditRole):
            return self._data[index.row()][index.column()]

        return None

    def setData(self, index, value, role = qtc.Qt.EditRole) -> object | None:
        """Set the data at the given index for editing"""
        if index.isValid() and role == qtc.Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        else:
            return False

    def flags(self, index) -> object:
        """Return the flags attached to the given index"""
        if not index.isValid():
            return qtc.Qt.ItemIsEnabled

        if index not in self.read_only_indexes:
            return super().flags(index) | qtc.Qt.ItemIsEditable
        else:
            return super().flags(index)

    def headerData(self, section, orientation, role=qtc.Qt.DisplayRole) -> object | str | None:
        """Return the header labels"""
        if role == qtc.Qt.DisplayRole and orientation == qtc.Qt.Horizontal:
            return self._headers[section]
        else:
            return super().headerData(section, orientation, role)

    def insert_file(self, position, rows, file_name, parent=qtc.QModelIndex()) -> None:
        """Insert a new row into the table"""
        self.beginInsertRows(parent, position, position + rows - 1)
        for _ in range(rows):
            new_row = [file_name, ""]
            self._data.insert(position, new_row)
        self.endInsertRows()

    def remove_file(self, position, rows, parent=qtc.QModelIndex()) -> None:
        """Remove a single row into the table"""
        self.beginRemoveRows(parent, position, position + rows - 1)
        for _ in range(rows):
            del(self._data[position])
        self.endRemoveRows()

class ManualMediaFileUpdate(qtw.QDialog):
    """
    Pop-up window to allow user to select media files they wish to update.
    """

    def __init__(self, parent=None):
        # The modal=True makes sure the user cannot click the main screen until they close the popup
        super().__init__(parent, modal=True)
        self.setWindowTitle("Media File Select")
        self.resize(800, 400)

        #self.table_model = MediaFileTable(None, ['Directory', 'Current File Name', 'New File Name'])

        # widgets
        self.add_files_btn = qtw.QPushButton('Add File(s)', self)
        self.remove_file_btn = qtw.QPushButton('Remove File(s)', self)
        self.update_files_btn = qtw.QPushButton('Update File(s)', self)
        cancel_btn = qtw.QPushButton('Cancel', self)
        cancel_btn.clicked.connect(self.close)

        self.table_view = qtw.QTableView(self)
        self.table_view.setSortingEnabled(True)

        # layout
        button_layout = qtw.QVBoxLayout()
        button_layout.addWidget(self.add_files_btn)
        button_layout.addWidget(self.remove_file_btn)
        button_layout.addWidget(self.update_files_btn)
        button_layout.addWidget(cancel_btn)

        main_layout = qtw.QHBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table_view)
        self.setLayout(main_layout)
