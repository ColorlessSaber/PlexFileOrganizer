from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
import pathlib

class MediaFileTable(qtc.QAbstractTableModel):
    """A table to allow user to view and modify what the file's new name should be"""

    def __init__(self, read_only_indexes: list, current_media_file_list: list = None, column_names: list = None):
        super().__init__()
        if current_media_file_list is None:
            current_media_file_list = []
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

    def insert_file(self, position, rows, row_data, parent=qtc.QModelIndex()) -> None:
        """Insert a new row into the table"""
        self.beginInsertRows(parent, position, position + rows - 1)
        for _ in range(rows):
            self._data.insert(position, row_data)
        self.endInsertRows()

    def remove_file(self, position, rows, parent=qtc.QModelIndex()) -> None:
        """Remove a single row into the table"""
        self.beginRemoveRows(parent, position, position + rows - 1)
        for _ in range(rows):
            del(self._data[position])
        self.endRemoveRows()

    def send_data(self) -> None:
        """
        Send the list of files off via a signal to be processed.
        """
        # TODO write in code later to send it off via signal.
        for row in self._data:
            print(row)

class ManualMediaFileUpdate(qtw.QDialog):
    """
    Pop-up window to allow user to select media files they wish to update.
    """

    def __init__(self, parent=None):
        # The modal=True makes sure the user cannot click the main screen until they close the popup
        super().__init__(parent, modal=True)
        self.setWindowTitle("Media File Select")
        self.resize(800, 400)

        # widgets
        self.btn_add_files = qtw.QPushButton('Add File(s)', self)
        self.btn_add_files.clicked.connect(self.select_files)
        self.btn_remove_file = qtw.QPushButton('Remove File(s)', self)
        self.btn_remove_file.setEnabled(False)
        self.btn_update_files = qtw.QPushButton('Update File(s)', self)
        self.btn_update_files.clicked.connect(self.update_files)
        self.btn_update_files.setEnabled(False)
        cancel_btn = qtw.QPushButton('Cancel', self)
        cancel_btn.clicked.connect(self.close)

        self.table_view = qtw.QTableView(self)
        self.table_view.setSortingEnabled(False)
        self.model =  MediaFileTable(
            ['Current File Name'],
            None,
            ['Directory', 'Current File Name', 'New File Name', 'Format Type']
        )
        self.table_view.setModel(self.model)
        self.table_view.setColumnHidden(0, True)
        self.table_view.setColumnHidden(3, True)

        # layout
        button_layout = qtw.QVBoxLayout()
        button_layout.addWidget(self.btn_add_files)
        button_layout.addWidget(self.btn_remove_file)
        button_layout.addWidget(self.btn_update_files)
        button_layout.addWidget(cancel_btn)

        main_layout = qtw.QHBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table_view)
        self.setLayout(main_layout)

    @qtc.Slot()
    def select_files(self) -> None:
        """
        Opens file dialog to allow user to select media files they wish to update, and
        adds them to the table.
        """
        selected_files, _ = qtw.QFileDialog.getOpenFileNames(
            self,
            "Select Files...",
            qtc.QDir.homePath(),
        "Media Files (*.mkv *.mp4 *.avi)"
        )

        if selected_files:
            for file in selected_files:
                self.model.insert_file(position=self.model.rowCount(), rows=1, row_data=[
                    str(pathlib.Path(file).parent),
                    pathlib.Path(file).stem,
                    "",
                    pathlib.Path(file).suffix]
                                       )

            self.table_view.resizeColumnsToContents()
            self.btn_remove_file.setEnabled(True)
            self.btn_update_files.setEnabled(True)

    @qtc.Slot()
    def update_files(self) -> None:
        """
        Sends off the list of files that will be updated and then closes the window.
        """
        self.model.send_data()