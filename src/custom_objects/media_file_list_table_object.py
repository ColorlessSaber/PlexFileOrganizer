from PySide6 import QtCore as qtc
from typing import Any
from .generic_pyside_objects import GenericTable

class MediaFileListTableObject(GenericTable):

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
            del self._data[position]
        self.endRemoveRows()

    def extract_data(self) -> list[Any]:
        """
        Returns the data that is stored in the table
        """
        return self._data