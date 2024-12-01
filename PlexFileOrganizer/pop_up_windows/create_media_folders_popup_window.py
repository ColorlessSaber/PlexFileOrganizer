"""
Pop-up window to allow user to create folder(s) per media type-TV show or movie
"""
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

class CreateMediaFolders(qtw.QDialog):

    def __init__(self, parent=None):
        # The modal=True makes sure the user cannot click the main screen until they close the popup
        super().__init__(parent, modal=True)
        self.setWindowTitle('Create Media Folder(s)')

        # widgets
        self.new_or_existing_group = qtw.QGroupBox('New Or Existing?')
        self.new_media_folder_select = qtw.QRadioButton('New', self)
        self.existing_media_folder_select = qtw.QRadioButton('Existing', self)
        self.new_or_existing_group.setLayout(qtw.QHBoxLayout())
        self.new_or_existing_group.layout().addWidget(self.new_media_folder_select)
        self.new_or_existing_group.layout().addWidget(self.existing_media_folder_select)

        self.media_type_group = qtw.QGroupBox('Media Type')
        self.media_type_movie_select = qtw.QRadioButton('Movie', self)
        self.media_type_tv_select = qtw.QRadioButton('TV Show', self)
        self.media_type_group.setLayout(qtw.QHBoxLayout())
        self.media_type_group.layout().addWidget(self.media_type_movie_select)
        self.media_type_group.layout().addWidget(self.media_type_tv_select)

        media_inform_form = qtw.QFormLayout()
        self.media_title = qtw.QLineEdit(self)
        self.season_number = qtw.QLineEdit(self)
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
        self.accept_btn.clicked.connect(self.accept)

        self.cancel_btn = qtw.QPushButton('Cancel', self)
        self.cancel_btn.clicked.connect(self.reject)

        # layout
        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(self.new_or_existing_group)
        main_layout.addWidget(self.media_type_group)
        main_layout.addLayout(media_inform_form)
        main_layout.addLayout(extra_folder_layout)
        main_layout.addWidget(self.accept_btn)
        main_layout.addWidget(self.cancel_btn)
        self.setLayout(main_layout)

    def accept(self):
        """Runs when accept button is pressed"""
        print('hello')
        super().accept()
