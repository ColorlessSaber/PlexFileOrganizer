"""
Pop-up window to allow user to add more folders to an existing media folder
"""
from PySide6 import (
    QtWidgets as qtw,
    QtGui as qtg,
    QtCore as qtc)

class ModifiedMediaFolderWindow(qtw.QDialog):
    signal_initiate_scan_of_media_folder = qtc.Signal(object)

    def __init__(self, parent=None):
        """
        Dialog window to allow user to select an existing Media Folder and then after the scan of the folder, select
        what new folders to add to it--Extra folders and or another TV show season folder--or remove folders from the
        Media Folder.

        :param parent: The parent window the dialog window will be linked to.
        """
        # The modal=True makes sure the user cannot click the main screen until they close the popup
        super().__init__(parent, modal=True)
        self.setWindowTitle('Modified Existing Media Folder')

        # widgets
        select_directory_layout = qtw.QGridLayout()
        self.btn_select_directory = qtw.QPushButton('Select Media Folder', self)
        self.select_directory_label = qtw.QLabel('', self)
        self.btn_select_directory.clicked.connect(self.select_media_folder)
        select_directory_layout.addWidget(self.btn_select_directory, 0, 0)
        select_directory_layout.addWidget(self.select_directory_label, 0, 1, 0, 2)

        self.media_type_group = qtw.QGroupBox('Media Type')
        self.media_type_movie_select = qtw.QRadioButton('Movie', self)
        self.media_type_tv_select = qtw.QRadioButton('TV Show', self)
        self.media_type_group.setLayout(qtw.QHBoxLayout())
        self.media_type_group.layout().addWidget(self.media_type_movie_select)
        self.media_type_group.layout().addWidget(self.media_type_tv_select)

        media_inform_form = qtw.QFormLayout()
        self.media_title = qtw.QLineEdit(self)
        self.number_of_seasons = qtw.QLineEdit(self)
        self.number_of_seasons.setValidator(qtg.QIntValidator(0, 100))
        self.number_of_seasons.setEnabled(False)
        media_inform_form.addRow('Title:', self.media_title)
        media_inform_form.addRow('Number of Seasons:', self.number_of_seasons)

        self.cb_trailers = qtw.QCheckBox('Trailers', self)
        self.cb_behind_the_scenes = qtw.QCheckBox('Behind The Scenes', self)
        self.cb_deleted_scenes = qtw.QCheckBox('Deleted Scenes', self)
        self.cb_featurettes = qtw.QCheckBox('Featurettes', self)
        self.cb_interviews = qtw.QCheckBox('Interviews', self)
        self.cb_scenes = qtw.QCheckBox('Scenes', self)
        self.cb_shorts = qtw.QCheckBox('shorts', self)
        self.cb_other = qtw.QCheckBox('Other', self)
        extra_folder_layout = qtw.QGridLayout()
        extra_folder_layout.addWidget(self.cb_trailers, 0, 0)
        extra_folder_layout.addWidget(self.cb_behind_the_scenes, 0, 1)
        extra_folder_layout.addWidget(self.cb_deleted_scenes, 0, 2)
        extra_folder_layout.addWidget(self.cb_featurettes, 0, 3)
        extra_folder_layout.addWidget(self.cb_interviews, 1, 0)
        extra_folder_layout.addWidget(self.cb_scenes, 1, 1)
        extra_folder_layout.addWidget(self.cb_shorts, 1, 2)
        extra_folder_layout.addWidget(self.cb_other, 1, 3)

        self.btn_accept = qtw.QPushButton('Accept', self)
        self.btn_accept.setEnabled(False)
        self.btn_accept.clicked.connect(self.accept)

        self.btn_cancel = qtw.QPushButton('Cancel', self)
        self.btn_cancel.clicked.connect(self.reject)

        # Set up the layout of window
        main_layout = qtw.QVBoxLayout()
        main_layout.addLayout(select_directory_layout)
        main_layout.addWidget(self.media_type_group)
        main_layout.addLayout(media_inform_form)
        main_layout.addLayout(extra_folder_layout)
        main_layout.addWidget(self.btn_accept)
        main_layout.addWidget(self.btn_cancel)
        self.setLayout(main_layout)

    @qtc.Slot(object)
    def load_existing_media_folder_info(self, media_file_information):
        print("Loading Existing Media Folder")
        print(media_file_information)

    def select_media_folder(self):
        media_folder_dir = qtw.QFileDialog.getExistingDirectory(
            self,
            'Select Media Folder...',
            qtc.QDir.homePath()
        )

        if media_folder_dir: # confirm the user selected a directory
            self.signal_initiate_scan_of_media_folder.emit(media_folder_dir)