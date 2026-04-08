from collections import namedtuple
from PySide6 import (
    QtCore as qtc,
    QtWidgets as qtw,
)
from .generic_pyside_objects import GenericTableView

class MediaFileListTableView(GenericTableView):
    """
    The media file list table view
    """
    signal_media_file = qtc.Signal(object)

    def context_menu(self, pos: qtc.QPoint) -> None:
        MediaFileSelectionInfo = namedtuple(
            "MediaFileSelectionInfo",
            ["num_of_indexes", "start_row"]
        )

        menu = qtw.QMenu()
        remove_media_file_action = menu.addAction("") # Will add name based on if user selected multiple or single files below
        if len(self.selectedIndexes()) == 1:
            remove_media_file_action.setText("Remove Media File")
        else:
            remove_media_file_action.setText("Remove Selected Media Files")

        action = menu.exec_(self.mapToGlobal(pos))
        if action == remove_media_file_action:
            print(f"number of index selected: {len(self.selectedIndexes())}, row: {self.selectedIndexes()[0].row()}")
            self.signal_media_file.emit(
                MediaFileSelectionInfo(
                    num_of_indexes=len(self.selectedIndexes()),
                    start_row=self.selectedIndexes()[0].row()
                )
            )
