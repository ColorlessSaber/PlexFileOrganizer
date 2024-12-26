"""
Pop-up window to allow user to create folder(s) per media type-TV show or movie
"""
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtCore as qtc

class CreateMediaFolders(qtw.QDialog):

    def __init__(self, create_media_folders_section, parent=None):
        """
        Dialog window to allow user to select if media folder is existing or not, movie or tv show,
        information about the media, and what Extra Folders they wish to create/add.

        :param create_media_folders_section: A dict to hold the inputs and information the user entered
        :param parent:
        """
        # The modal=True makes sure the user cannot click the main screen until they close the popup
        super().__init__(parent, modal=True)
        self.setWindowTitle('Create Media Folder(s)')

        # variables
        self.create_media_folders_section = create_media_folders_section
        self.selected_directory = ''

        # widgets
        select_directory_layout = qtw.QGridLayout()
        self.select_directory_btn = qtw.QPushButton('Select Directory', self)
        self.select_directory_btn.clicked.connect(self.select_directory_popup)
        self.select_directory_label = qtw.QLabel('', self)
        select_directory_layout.addWidget(self.select_directory_btn, 0, 0)
        select_directory_layout.addWidget(self.select_directory_label, 0, 1, 0, 2)

        self.new_or_existing_group = qtw.QGroupBox('New Or Existing?')
        self.new_media_folder_select = qtw.QRadioButton('New', self)
        self.new_media_folder_select.toggled.connect(self.enable_or_disable_accept_btn)
        self.existing_media_folder_select = qtw.QRadioButton('Existing', self)
        self.existing_media_folder_select.toggled.connect(self.enable_or_disable_accept_btn)
        self.new_or_existing_group.setLayout(qtw.QHBoxLayout())
        self.new_or_existing_group.layout().addWidget(self.new_media_folder_select)
        self.new_or_existing_group.layout().addWidget(self.existing_media_folder_select)

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
        self.season_number = qtw.QLineEdit(self)
        self.season_number.setValidator(qtg.QIntValidator(0, 100))
        self.season_number.setEnabled(False)
        media_inform_form.addRow('Title:', self.media_title)
        media_inform_form.addRow('Season #:', self.season_number)

        self.extra_folders_option_group = qtw.QGroupBox('Extra Folder(s)')
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

        # layout
        main_layout = qtw.QVBoxLayout()
        main_layout.addLayout(select_directory_layout)
        main_layout.addWidget(self.new_or_existing_group)
        main_layout.addWidget(self.media_type_group)
        main_layout.addLayout(media_inform_form)
        main_layout.addLayout(extra_folder_layout)
        main_layout.addWidget(self.accept_btn)
        main_layout.addWidget(self.cancel_btn)
        self.setLayout(main_layout)

    @qtc.Slot()
    def enable_or_disable_accept_btn(self):
        if (self.new_media_folder_select.isChecked() or self.existing_media_folder_select.isChecked()) and \
                (self.media_type_tv_select.isChecked() or self.media_type_tv_select) and (len(self.media_title.text())>0):
            self.accept_btn.setEnabled(True)
        else:
            self.accept_btn.setEnabled(False)

    @qtc.Slot()
    def enable_or_disable_season_number_line_edit(self):
        if self.media_type_movie_select.isChecked():
            self.season_number.setEnabled(False)
        elif self.media_type_tv_select.isChecked():
            self.season_number.setEnabled(True)
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

    @qtc.Slot()
    def accept(self):
        """Runs when accept button is pressed"""
        if self.selected_directory:
            self.create_media_folders_section['directory'] = self.selected_directory
            self.create_media_folders_section['new or existing'] = 'new' if self.new_media_folder_select.isChecked() else 'existing'
            self.create_media_folders_section['movie or tv'] = 'movie' if self.media_type_movie_select.isChecked() else 'tv'
            self.create_media_folders_section['media title'] = self.media_title.text()
            self.create_media_folders_section['season num'] = self.season_number.text()
            self.create_media_folders_section['extra folders']['trailer'] = self.trailers_cb.isChecked()
            self.create_media_folders_section['extra folders']['behind the scenes'] = self.behind_the_scenes_cb.isChecked()
            self.create_media_folders_section['extra folders']['featurettes'] = self.featurettes_cb.isChecked()
            self.create_media_folders_section['extra folders']['interviews '] = self.interviews_cb.isChecked()
            self.create_media_folders_section['extra folders']['scenes'] = self.scenes_cb.isChecked()
            self.create_media_folders_section['extra folders']['shorts'] = self.shorts_cb.isChecked()
            self.create_media_folders_section['extra folders']['other'] = self.other_cb.isChecked()
            super().accept()
        else:
            qtw.QMessageBox.critical(self, 'No Directory Selected', 'Please select a directory to create folder(s) in.')
