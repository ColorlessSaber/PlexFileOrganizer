"""
Pop-up window to allow user to create a media folder for a movie or TV show
"""
from ..classes import GenerateMediaFolder
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

class CreateMediaFolder(qtw.QDialog):
    signal_initiate_create_media_folder = qtc.Signal(object)
    signal_reset_progress_bar = qtc.Signal()

    def __init__(self, parent=None):
        """
        A dialog window to allow user to generate a new Media Folder. Able to selection if it's a movie or tv show,
        how many seasons if it is a tv show, and which Extra Folders they wish to make.

        :param parent: The parent window the dialog window will be linked to.
        """
        # The modal=True makes sure the user cannot click the main screen until they close the popup
        super().__init__(parent, modal=True)
        self.setWindowTitle('Create Media Folder(s)')

        # widgets
        select_directory_layout = qtw.QGridLayout()
        btn_select_directory = qtw.QPushButton('Select Directory', self)
        btn_select_directory.clicked.connect(self.select_directory_popup)
        self.select_directory_label = qtw.QLabel('', self)
        select_directory_layout.addWidget(btn_select_directory, 0, 0)
        select_directory_layout.addWidget(self.select_directory_label, 0, 1, 0, 2)

        self.media_type_group = qtw.QGroupBox('Media Type')
        self.rb_media_type_movie_select = qtw.QRadioButton('Movie', self)
        self.rb_media_type_movie_select.setChecked(True)
        self.rb_media_type_movie_select.toggled.connect(self.enable_or_disable_season_number_line_edit)
        self.rb_media_type_movie_select.toggled.connect(self.enable_or_disable_create_btn)
        self.rb_media_type_tv_select = qtw.QRadioButton('TV Show', self)
        self.rb_media_type_tv_select.toggled.connect(self.enable_or_disable_season_number_line_edit)
        self.rb_media_type_tv_select.toggled.connect(self.enable_or_disable_create_btn)
        self.media_type_group.setLayout(qtw.QHBoxLayout())
        self.media_type_group.layout().addWidget(self.rb_media_type_movie_select)
        self.media_type_group.layout().addWidget(self.rb_media_type_tv_select)

        media_inform_form = qtw.QFormLayout()
        self.le_media_title = qtw.QLineEdit(self)
        self.le_media_title.textChanged.connect(self.enable_or_disable_create_btn)
        self.number_of_seasons = qtw.QSpinBox(self, value=1, maximum=100, minimum=1)
        self.number_of_seasons.setEnabled(False)
        media_inform_form.addRow('Title:', self.le_media_title)
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

        self.btn_create = qtw.QPushButton('Create', self)
        self.btn_create.setEnabled(False)
        self.btn_create.clicked.connect(self.start_folder_generation)

        btn_cancel = qtw.QPushButton('Cancel', self)
        btn_cancel.clicked.connect(self.reject)

        # Set up the layout of window
        main_layout = qtw.QVBoxLayout()
        main_layout.addLayout(select_directory_layout)
        main_layout.addWidget(self.media_type_group)
        main_layout.addLayout(media_inform_form)
        main_layout.addLayout(extra_folder_layout)
        main_layout.addWidget(self.btn_create)
        main_layout.addWidget(btn_cancel)
        self.setLayout(main_layout)

    @qtc.Slot()
    def enable_or_disable_create_btn(self) -> None:
        if (self.rb_media_type_tv_select.isChecked() or self.rb_media_type_tv_select) and (len(self.le_media_title.text()) > 0) \
                and (self.select_directory_label.text() != ''):
            self.btn_create.setEnabled(True)
        else:
            self.btn_create.setEnabled(False)

    @qtc.Slot()
    def enable_or_disable_season_number_line_edit(self) -> None:
        if self.rb_media_type_movie_select.isChecked():
            self.number_of_seasons.setEnabled(False)
        elif self.rb_media_type_tv_select.isChecked():
            self.number_of_seasons.setEnabled(True)
        else:
            pass

    @qtc.Slot()
    def select_directory_popup(self) -> None:
        directory = qtw.QFileDialog.getExistingDirectory(
            self,
            'Select folder...',
            qtc.QDir.homePath()
        )

        if directory:
            self.select_directory_label.setText(directory)
            self.enable_or_disable_create_btn()

    @qtc.Slot()
    def start_folder_generation(self) -> None:
        """
        Create the object that holds the information about the new media folder and send it off before
        closing the window.
        """
        new_media_folder_info = GenerateMediaFolder()

        new_media_folder_info.directory = self.select_directory_label.text()
        new_media_folder_info.media_title = self.le_media_title.text()
        new_media_folder_info.media_type = 'movie' if self.rb_media_type_movie_select.isChecked() else 'tv'
        new_media_folder_info.number_of_seasons = int(self.number_of_seasons.text()) if self.number_of_seasons.text() else 0
        new_media_folder_info.extra_folders['trailers'] = self.cb_trailers.isChecked()
        new_media_folder_info.extra_folders['behind the scenes'] = self.cb_behind_the_scenes.isChecked()
        new_media_folder_info.extra_folders['deleted scenes'] = self.cb_deleted_scenes.isChecked()
        new_media_folder_info.extra_folders['featurettes'] = self.cb_featurettes.isChecked()
        new_media_folder_info.extra_folders['interviews '] = self.cb_interviews.isChecked()
        new_media_folder_info.extra_folders['scenes'] = self.cb_scenes.isChecked()
        new_media_folder_info.extra_folders['shorts'] = self.cb_shorts.isChecked()
        new_media_folder_info.extra_folders['other'] = self.cb_other.isChecked()


        self.signal_initiate_create_media_folder.emit(new_media_folder_info)

    @qtc.Slot()
    def messagebox_media_folder_already_exists(self) -> None:
        """
        Launches the messagebox to inform user the media folder they wish to make already exists.
        Will reset the progress bar once user closes the messagebox window.

        :return:
        """
        response = qtw.QMessageBox.information(
            self,
            'Media Folder Already Exists',
            'The Media Folder you wish to make already exists. Please click "ok" to cancel creation of Media Folder.'
        )

        if response == qtw.QMessageBox.Ok:
            self.signal_reset_progress_bar.emit()

    @qtc.Slot()
    def messagebox_media_folder_creation_complete(self) -> None:
        """
        Launches the messagebox to inform user the creation of the media folder is complete.
        Will reset the progress bar and close the "create media folder" window once user closes the messagebox window.

        :return:
        """
        response = qtw.QMessageBox.information(
            self,
            'Create Media Folder Complete!',
            'Finished creating the media folder in the directory.'
        )

        if response == qtw.QMessageBox.Ok:
            self.signal_reset_progress_bar.emit()
            self.accept()
