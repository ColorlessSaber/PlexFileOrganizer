"""
Pop-up window to allow user to create a media folder for a movie or TV show
"""
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtCore as qtc

class CreateMediaFolder(qtw.QDialog):

    def __init__(self, new_media_folder_info, parent=None):
        """
        A dialog window to allow user to generate a new Media Folder. Able to selection if it's a movie or tv show,
        how many seasons if it is a tv show, and which Extra Folders they wish to make.

        :param new_media_folder_info: A class that will hold the information for the new Media Folder
        :param parent: The parent window the dialog window will be linked to.
        """
        # The modal=True makes sure the user cannot click the main screen until they close the popup
        super().__init__(parent, modal=True)
        self.setWindowTitle('Create Media Folder(s)')

        # variables
        self.new_media_folder_info = new_media_folder_info
        self.selected_directory = ''

        # widgets
        select_directory_layout = qtw.QGridLayout()
        self.select_directory_btn = qtw.QPushButton('Select Directory', self)
        self.select_directory_btn.clicked.connect(self.select_directory_popup)
        self.select_directory_label = qtw.QLabel('', self)
        select_directory_layout.addWidget(self.select_directory_btn, 0, 0)
        select_directory_layout.addWidget(self.select_directory_label, 0, 1, 0, 2)

        self.media_type_group = qtw.QGroupBox('Media Type')
        self.media_type_movie_select = qtw.QRadioButton('Movie', self)
        self.media_type_movie_select.toggled.connect(self.enable_or_disable_season_number_line_edit)
        self.media_type_movie_select.toggled.connect(self.enable_or_disable_accept_btn)
        self.media_type_tv_select = qtw.QRadioButton('TV Show', self)
        self.media_type_tv_select.toggled.connect(self.enable_or_disable_season_number_line_edit)
        self.media_type_tv_select.toggled.connect(self.enable_or_disable_accept_btn)
        self.media_type_group.setLayout(qtw.QHBoxLayout())
        self.media_type_group.layout().addWidget(self.media_type_movie_select)
        self.media_type_group.layout().addWidget(self.media_type_tv_select)

        media_inform_form = qtw.QFormLayout()
        self.media_title = qtw.QLineEdit(self)
        self.media_title.textChanged.connect(self.enable_or_disable_accept_btn)
        self.number_of_seasons = qtw.QLineEdit(self)
        self.number_of_seasons.setValidator(qtg.QIntValidator(0, 100))
        self.number_of_seasons.setEnabled(False)
        media_inform_form.addRow('Title:', self.media_title)
        media_inform_form.addRow('Number of Seasons:', self.number_of_seasons)

        self.trailers_cb = qtw.QCheckBox('Trailers', self)
        self.behind_the_scenes_cb = qtw.QCheckBox('Behind The Scenes', self)
        self.deleted_scenes_cb = qtw.QCheckBox('Deleted Scenes', self)
        self.featurettes_cb = qtw.QCheckBox('Featurettes', self)
        self.interviews_cb = qtw.QCheckBox('Interviews', self)
        self.scenes_cb = qtw.QCheckBox('Scenes', self)
        self.shorts_cb = qtw.QCheckBox('shorts', self)
        self.other_cb = qtw.QCheckBox('Other', self)
        extra_folder_layout = qtw.QGridLayout()
        extra_folder_layout.addWidget(self.trailers_cb, 0, 0)
        extra_folder_layout.addWidget(self.behind_the_scenes_cb, 0, 1)
        extra_folder_layout.addWidget(self.deleted_scenes_cb, 0, 2)
        extra_folder_layout.addWidget(self.featurettes_cb, 0, 3)
        extra_folder_layout.addWidget(self.interviews_cb, 1, 0)
        extra_folder_layout.addWidget(self.scenes_cb, 1, 1)
        extra_folder_layout.addWidget(self.shorts_cb, 1, 2)
        extra_folder_layout.addWidget(self.other_cb, 1, 3)

        self.accept_btn = qtw.QPushButton('Accept', self)
        self.accept_btn.setEnabled(False)
        self.accept_btn.clicked.connect(self.accept)

        self.cancel_btn = qtw.QPushButton('Cancel', self)
        self.cancel_btn.clicked.connect(self.reject)

        # Set up the layout of window
        main_layout = qtw.QVBoxLayout()
        main_layout.addLayout(select_directory_layout)
        main_layout.addWidget(self.media_type_group)
        main_layout.addLayout(media_inform_form)
        main_layout.addLayout(extra_folder_layout)
        main_layout.addWidget(self.accept_btn)
        main_layout.addWidget(self.cancel_btn)
        self.setLayout(main_layout)

    @qtc.Slot()
    def enable_or_disable_accept_btn(self):
        if (self.media_type_tv_select.isChecked() or self.media_type_tv_select) and (len(self.media_title.text())>0) \
                and self.selected_directory:
            self.accept_btn.setEnabled(True)
        else:
            self.accept_btn.setEnabled(False)

    @qtc.Slot()
    def enable_or_disable_season_number_line_edit(self):
        if self.media_type_movie_select.isChecked():
            self.number_of_seasons.setEnabled(False)
        elif self.media_type_tv_select.isChecked():
            self.number_of_seasons.setEnabled(True)
        else:
            pass

    @qtc.Slot()
    def select_directory_popup(self):
        directory = qtw.QFileDialog.getExistingDirectory(
            self,
            'Select folder...',
            qtc.QDir.homePath()
        )

        if directory:
            self.selected_directory = directory
            self.select_directory_label.setText(directory)
            self.enable_or_disable_accept_btn()

    @qtc.Slot()
    def accept(self):
        """
        Runs when accept button is pressed
        :return:
        """
        self.new_media_folder_info.directory = self.selected_directory
        self.new_media_folder_info.media_title = self.media_title.text()
        self.new_media_folder_info.movie_or_tv = 'movie' if self.media_type_movie_select.isChecked() else 'tv'
        self.new_media_folder_info.number_of_seasons = int(self.number_of_seasons.text()) if self.number_of_seasons.text() else 0
        self.new_media_folder_info.extra_folders['trailers'] = self.trailers_cb.isChecked()
        self.new_media_folder_info.extra_folders['behind the scenes'] = self.behind_the_scenes_cb.isChecked()
        self.new_media_folder_info.extra_folders['deleted scenes'] = self.deleted_scenes_cb.isChecked()
        self.new_media_folder_info.extra_folders['featurettes'] = self.featurettes_cb.isChecked()
        self.new_media_folder_info.extra_folders['interviews '] = self.interviews_cb.isChecked()
        self.new_media_folder_info.extra_folders['scenes'] = self.scenes_cb.isChecked()
        self.new_media_folder_info.extra_folders['shorts'] = self.shorts_cb.isChecked()
        self.new_media_folder_info.extra_folders['other'] = self.other_cb.isChecked()
        super().accept()
