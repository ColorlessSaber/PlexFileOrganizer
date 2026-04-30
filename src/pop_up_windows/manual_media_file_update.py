from ..custom_objects import (
    MediaListTable,
    MediaListTableView,
)
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
import pathlib
from typing import NamedTuple

class ManualMediaFileUpdate(qtw.QDialog):
    """
    Pop-up window to allow user to select media files they wish to update.
    """

    signal_initiate_manual_update = qtc.Signal(list)
    signal_check_list_of_files_for_duplicates = qtc.Signal(list)
    signal_reset_progress_bar = qtc.Signal()

    def __init__(self, parent=None):
        # The modal=True makes sure the user cannot click the main screen until they close the popup
        super().__init__(parent, modal=True)
        self.setWindowTitle("Media File Select")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        # Files table with buttons
        self.btn_add_files = qtw.QPushButton("Add File(s)", self)
        self.btn_add_files.clicked.connect(self.select_files)
        self.btn_clear_table = qtw.QPushButton("Clear Table", self)
        self.btn_clear_table.clicked.connect(self.clear_table)
        self.btn_clear_table.setEnabled(False)

        self.table_view = MediaListTableView(self)
        self.table_view.setSortingEnabled(False)
        self.model = MediaListTable(
            [0, 1, 3],
            None,
            ["Directory", "Current File Name", "New File Name", "Format Type"],
        )
        self.table_view.setModel(self.model)
        self.table_view.signal_media_file.connect(self.remove_files)

        # Hiding 'Directory' and 'Format Type' from user view for they are storing the respective
        # information to be used during the processes of updating the files.
        self.table_view.setColumnHidden(0, True)
        self.table_view.setColumnHidden(3, True)

        table_buttons_layout = qtw.QHBoxLayout()
        table_buttons_layout.addWidget(self.btn_add_files)
        table_buttons_layout.addWidget(self.btn_clear_table)

        table_with_buttons_layout = qtw.QVBoxLayout()
        table_with_buttons_layout.addLayout(table_buttons_layout)
        table_with_buttons_layout.addWidget(self.table_view)

        groupbox_file_table = qtw.QGroupBox("") # Left name out for don't see a reason to identify the group
        groupbox_file_table.setLayout(table_with_buttons_layout)
        groupbox_file_table.setStyleSheet("""
            QGroupBox {
                border: 2px solid grey;
                border-radius: 5px;
            }
        """)

        # buttons at bottom
        self.btn_update_files = qtw.QPushButton("Update File(s)", self)
        self.btn_update_files.clicked.connect(self.first_stage_update_process)
        self.btn_update_files.setEnabled(False)
        self.btn_close = qtw.QPushButton("Cancel", self)
        self.btn_close.clicked.connect(self.reject)
        update_or_close_buttons_layout = qtw.QHBoxLayout()
        update_or_close_buttons_layout.addWidget(self.btn_update_files)
        update_or_close_buttons_layout.addWidget(self.btn_close)

        # layout
        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(groupbox_file_table)
        main_layout.addLayout(update_or_close_buttons_layout)
        self.setLayout(main_layout)

    @qtc.Slot()
    def select_files(self) -> None:
        """
        Opens file dialog to allow user to select media files they wish to update, and
        adds them to the table.

        :return:
        """
        selected_files, _ = qtw.QFileDialog.getOpenFileNames(
            self,
            "Select Files...",
            qtc.QDir.homePath(),
            "Media Files (*.mkv *.mp4 *.avi)",
        )

        if selected_files:
            for file in selected_files:
                self.model.insert_file(
                    position=self.model.rowCount(),
                    rows=1,
                    row_data=[
                        str(pathlib.Path(file).parent),
                        pathlib.Path(file).stem,
                        pathlib.Path(
                            file
                        ).stem,  # The original name is the default. Allowing user to make necessary changes to the original name
                        pathlib.Path(file).suffix,
                    ],
                )

            self.table_view.resizeColumnsToContents()
            self.btn_remove_file.setEnabled(True)
            self.btn_clear_table.setEnabled(True)
            self.btn_update_files.setEnabled(True)

    @qtc.Slot(object)
    def remove_files(self, selection_info: NamedTuple) -> None:
        """
        Removes selected file(s) from the table the user selected.

        :return:
        """
        selected_files = self.table_view.selectedIndexes()
        if selected_files:
            self.model.remove_file(
                position=selection_info.start_row,
                rows=selection_info.num_of_indexes
            )

    def clear_table(self) -> None:
        """
        Clears the table.

        :return:
        """
        number_of_rows = self.table_view.model().rowCount()
        if number_of_rows > 0:
            self.model.remove_file(position=0, rows=number_of_rows)

        self.btn_remove_file.setEnabled(False)
        self.btn_clear_table.setEnabled(False)
        self.btn_update_files.setEnabled(False)

    @qtc.Slot()
    def first_stage_update_process(self) -> None:
        """
        First stage of updating the media files.
        -- Inform the user that the program will not validate the media files that they are formated correctly.
        -- Sends the files out and check to see if there are duplicate rename file names.

        :return:
        """
        response = qtw.QMessageBox.warning(
            self,
            "Are you sure you want to update?",
            "The program will not validate that the media files you wish to update are formated correctly. Click Ok to continue.",
            buttons=qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel,
            defaultButton=qtw.QMessageBox.Ok,
        )

        if response == qtw.QMessageBox.Ok:
            self._enable_or_disable_buttons(False)

            data = self.model.extract_data()
            self.signal_check_list_of_files_for_duplicates.emit(data)

    @qtc.Slot(bool)
    def second_stage_update_process(
        self, there_are_no_duplicates_in_rename_file_list: bool
    ) -> None:
        """
        Second stage of update the media files.
        -- If there are no duplicate rename file names, send the data off to be processed.
        -- if there are duplicate rename file names, cancel operation and inform the user.

        :param there_are_no_duplicates_in_rename_file_list: True if there are no duplicate rename file names in list.
        :return:
        """
        if there_are_no_duplicates_in_rename_file_list:
            data = self.model.extract_data()
            self.signal_initiate_manual_update.emit(data)
        else:
            qtw.QMessageBox.warning(
                self,
                "There are duplicate rename file names.",
                "You are two or more files with matching rename file names. Please fix this to be able to manually update the media file name(s).",
                buttons=qtw.QMessageBox.Ok,
                defaultButton=qtw.QMessageBox.Ok,
            )
            self._enable_or_disable_buttons(True)

    @qtc.Slot()
    def messagebox_manual_update_media_files_complete(self) -> None:
        """
        Launches a messagebox to inform user the manual update of the media files is complete.
        Will reset the progress bar, enable all button widgets, and clear the table.

        :return:
        """
        response = qtw.QMessageBox.information(
            self,
            "Manual Update of Media Files Complete!",
            "Finished updating the media files in the directory. Please see console window for information on if any files were updated during the scan.",
        )

        if response == qtw.QMessageBox.Ok:
            self.signal_reset_progress_bar.emit()
            self._enable_or_disable_buttons(True)
            self.clear_table()

    @qtc.Slot()
    def enable_buttons_due_to_error(self) -> None:
        """
        Enables all button widgets due to error.

        :return:
        """
        self._enable_or_disable_buttons(True)

    def _enable_or_disable_buttons(self, enable_or_disable: bool) -> None:
        """
        Enables / disables the buttons widgets.

        :param enable_or_disable: Sets the enable / disable status
        :return:
        """
        self.btn_add_files.setEnabled(enable_or_disable)
        self.btn_remove_file.setEnabled(enable_or_disable)
        self.btn_clear_table.setEnabled(enable_or_disable)
        self.btn_update_files.setEnabled(enable_or_disable)
        self.btn_close.setEnabled(enable_or_disable)
