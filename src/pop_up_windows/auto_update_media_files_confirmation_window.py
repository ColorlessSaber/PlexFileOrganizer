"""
Pop-up window to warn user how the Auto-Update Media Files process work,
and get final confirmation that they wish to process, along with input if to update the files in
the extra folders as well
"""

from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtCore as qtc


class AutoUpdateMediaFilesWindow(qtw.QDialog):
    signal_initiate_auto_update = qtc.Signal(dict)

    def __init__(self, parent=None):
        """
        A dialog window that inform the users what happens when the program does an auto update of media files
        it finds. Also provides options that be selected that govern what the program will scan versus skip over.

        :param parent: The parent window the dialog window will be linked to.
        """
        # The modal=True makes sure the user cannot click the main screen until they close the popup
        super().__init__(parent, modal=True)
        self.setWindowTitle("Auto-Update Media Files Confirmation")
        self.setFixedWidth(900)
        self.setFixedHeight(600)

        # Labels
        label_information_of_process = qtw.QTextBrowser(self)
        label_information_of_process.setHtml(
            """
            <body>
            <p>
                Please read the following before proceeding to select a directory to Auto-Update Media Files in a selected
                directory and the available options.
            </p>
            <p><u>The program will make the following assumptions:</u></p>
            <ol>
                <li> The folder structure and the name of the folders follows Plex's recommended structure.</li>
                <li> Every media file has their own media folder; ie, all movie files aren't thrown into the same folder,
            they are in separate folders. </li>
                <li> The files in the TV season folder are in the correct chronological order by episode,
                from top to bottom. </li>
                <li> All files are single episodes; there isn’t a media file that represents two or more episodes.</li>
                <li> There aren't an TV episode or a movie  that is split cross two or more media files.</li>
            </ol>
            <p>
            If you wish to give custom names for files in an Extra Folder, or you know that a tv show file represents two
            or more episodes, or the files in a season folder aren’t in chronological order by episode; exit out of
            this window and click the “Manual-Update Media Files’ option on the main window.
            </p>
            <p><b>Auto Update Scanner Options</b></p>
            <ul>
                <li> <i>Update media files in Extra Folder(s)</i> -- the program will override any custom naming you
                gave to a file in a Extra Folder to the default naming convention for the folder they are in.
                EX: files in a Trailers folder will get ‘Trailer #.' </li>
            <ul>
            </body>
            """,
        )
        label_information_of_process.setAlignment(qtc.Qt.AlignmentFlag.AlignLeft)
        label_information_of_process.setFont(qtg.QFont("Arial", 16))

        # auto update scanner options
        self.cb_extra_folders_to_be_scanned = qtw.QCheckBox(
            "Update media files in Extra Folder(s)", self
        )
        auto_update_scanner_options_layout = qtw.QGridLayout()
        auto_update_scanner_options_layout.addWidget(self.cb_extra_folders_to_be_scanned, 0, 0)
        groupbox_auto_update_scanner_options = qtw.QGroupBox("Auto Update Scanner Options", self)
        groupbox_auto_update_scanner_options.setLayout(auto_update_scanner_options_layout)
        groupbox_auto_update_scanner_options.setStyleSheet("""
            QGroupBox {
                border: 2px solid grey;
                border-radius: 5px;
                padding-top: 16px;
                font-weight: bold;
            }
        """)


        # directory selection
        self.btn_select_directory = qtw.QPushButton("Select Directory", self)
        self.btn_select_directory.clicked.connect(self.select_directory_window)
        self.label_selected_directory = qtw.QLabel("", self)
        directory_selected_layout = qtw.QHBoxLayout()
        directory_selected_layout.addWidget(self.btn_select_directory)
        directory_selected_layout.addWidget(self.label_selected_directory)

        # buttons at the bottom
        self.btn_proceed = qtw.QPushButton("Proceed", self)
        self.btn_proceed.setEnabled(False)
        self.btn_proceed.clicked.connect(self.start_update_process)
        self.btn_cancel = qtw.QPushButton("Cancel", self)
        self.btn_cancel.clicked.connect(self.reject)
        proceed_cancel_button_layout = qtw.QHBoxLayout()
        proceed_cancel_button_layout.addWidget(self.btn_proceed)
        proceed_cancel_button_layout.addWidget(self.btn_cancel)

        # Set up the layout of window
        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(label_information_of_process)
        main_layout.addLayout(directory_selected_layout)
        main_layout.addWidget(groupbox_auto_update_scanner_options)
        main_layout.addLayout(proceed_cancel_button_layout)
        self.setLayout(main_layout)

    @qtc.Slot()
    def select_directory_window(self) -> None:
        """
        Open a directory selector window

        :return:
        """
        directory_selected_by_user = qtw.QFileDialog.getExistingDirectory(
            self, "Select folder...", qtc.QDir.homePath()
        )

        # confirm user selected a directory
        if directory_selected_by_user:
            self.btn_proceed.setEnabled(
                True
            )  # enable the button given user has selected a directory
            self.label_selected_directory.setText(directory_selected_by_user)

    def start_update_process(self) -> None:
        """
        Create the object that holds the information of what directory to scan and what options were selected
        and sends it off before closing the window.

        :return:
        """
        user_selected_dir_and_options = {
            "directory": self.label_selected_directory.text(),
            "scan_extra_folder": self.cb_extra_folders_to_be_scanned.isChecked(),
        }

        self.signal_initiate_auto_update.emit(user_selected_dir_and_options)

        self.accept()
