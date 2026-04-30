"""
Pop-up window to allow user to create a media folder for a movie or TV show
"""

from ..classes import GenerateMediaFolder
from ..custom_objects import MediaCategory
from PySide6 import QtWidgets as qtw, QtCore as qtc


class CreateMediaFolder(qtw.QDialog):
    signal_initiate_create_media_folder = qtc.Signal(object)
    signal_reset_progress_bar = qtc.Signal()

    def __init__(self, parent=None):
        """
        A dialog window to allow user to generate a new Media Folder. Able to selection if it's a movie or tv show,
        how many seasons if it is a TV show, and which Extra Folders they wish to make.

        :param parent: The parent window the dialog window will be linked to.
        """
        # The modal=True makes sure the user cannot click the main screen until they close the popup
        super().__init__(parent, modal=True)
        self.setWindowTitle("Create Media Folder(s)")

        # widgets
        ## select a directory
        select_directory_layout = qtw.QGridLayout()
        self.btn_select_directory = qtw.QPushButton("Select Directory", self)
        self.btn_select_directory.setFocusPolicy(qtc.Qt.FocusPolicy.NoFocus)
        self.btn_select_directory.clicked.connect(self.select_directory_popup)
        self.le_selected_directory = qtw.QLineEdit(self)
        self.le_selected_directory.setStyleSheet("""
            QLineEdit {
                border: 1px solid grey;
                border-radius: 5px;
            }
        """)
        self.le_selected_directory.textChanged.connect(self.enable_or_disable_create_btn)
        select_directory_layout.addWidget(self.btn_select_directory, 0, 0)
        select_directory_layout.addWidget(self.le_selected_directory, 0, 1, 0, 2)

        ## media information
        self.le_media_title = qtw.QLineEdit(self)
        self.le_media_title.textChanged.connect(self.enable_or_disable_create_btn)
        self.le_edition_tag = qtw.QLineEdit(self)
        media_title_layout = qtw.QGridLayout()
        media_title_layout.addWidget(qtw.QLabel("Title:", self), 0, 0)
        media_title_layout.addWidget(self.le_media_title, 0, 1)
        media_title_layout.addWidget(qtw.QLabel("Edition:", self), 1, 0)
        media_title_layout.addWidget(self.le_edition_tag, 1, 1)

        media_type_group = qtw.QGroupBox("Media Type")
        media_type_group.setObjectName("media_type_group")
        self.rb_media_type_movie_select = qtw.QRadioButton("Movie", self)
        self.rb_media_type_movie_select.setChecked(True)
        self.rb_media_type_movie_select.clicked.connect(
            self.enable_or_disable_tv_show_options
        )
        self.rb_media_type_tv_select = qtw.QRadioButton("TV Show", self)
        self.rb_media_type_tv_select.clicked.connect(
            self.enable_or_disable_tv_show_options
        )
        media_type_group.setLayout(qtw.QHBoxLayout())
        media_type_group.layout().addWidget(self.rb_media_type_movie_select)
        media_type_group.layout().addWidget(self.rb_media_type_tv_select)

        layout_media_information = qtw.QVBoxLayout()
        layout_media_information.setSpacing(20)
        layout_media_information.addLayout(media_title_layout)
        layout_media_information.addWidget(media_type_group)

        self.groupbox_media_information = qtw.QGroupBox("Media Information", self)
        self.groupbox_media_information.setObjectName("media_information")
        self.groupbox_media_information.setLayout(layout_media_information)
        self.groupbox_media_information.setStyleSheet("""
            #media_information {
                border: 2px solid grey;
                border-radius: 5px;
                padding-top: 16px;
                font-weight: bold;
            }
            #media_type_group {
                text-decoration: underline;
                font-size: 14px;
            }
            QLabel {
                text-decoration: underline;
            }
            QLineEdit {
                border: 1px solid grey;
                border-radius: 5px;
            }
        """)

        ## TV show options
        self.sb_number_of_seasons = qtw.QSpinBox(
            self, value=1, maximum=100, minimum=1, singleStep=1
        )
        self.cb_specials_season_folder = qtw.QCheckBox("Yes", self)
        label_number_of_seasons = qtw.QLabel("How many seasons to create?", self)
        label_number_of_seasons.setObjectName("number_of_seasons_label")
        label_generate_specials_folder = qtw.QLabel(
            "Generate Specials Season Folder?", self
        )
        label_generate_specials_folder.setObjectName("generate_specials_folder_label")
        tv_show_options_form = qtw.QFormLayout()
        tv_show_options_form.addRow(label_number_of_seasons, self.sb_number_of_seasons)
        tv_show_options_form.addRow(
            label_generate_specials_folder, self.cb_specials_season_folder
        )
        tv_show_options_form.setFormAlignment(qtc.Qt.AlignmentFlag.AlignLeft)
        self.groupbox_tv_show_options = qtw.QGroupBox("TV Show Options", self)
        self.groupbox_tv_show_options.setLayout(tv_show_options_form)
        self.groupbox_tv_show_options.setStyleSheet("""
            QGroupBox {
                border: 2px solid grey;
                border-radius: 5px;
                padding-top: 16px;
                font-weight: bold;
            }

            QLabel {
                text-decoration: underline;
            }
        """)
        self.groupbox_tv_show_options.setEnabled(False)

        ## extra folder options
        self.cb_trailers = qtw.QCheckBox("Trailers", self)
        self.cb_behind_the_scenes = qtw.QCheckBox("Behind The Scenes", self)
        self.cb_deleted_scenes = qtw.QCheckBox("Deleted Scenes", self)
        self.cb_featurettes = qtw.QCheckBox("Featurettes", self)
        self.cb_interviews = qtw.QCheckBox("Interviews", self)
        self.cb_scenes = qtw.QCheckBox("Scenes", self)
        self.cb_shorts = qtw.QCheckBox("shorts", self)
        self.cb_other = qtw.QCheckBox("Other", self)
        extra_folder_options_layout = qtw.QGridLayout()
        extra_folder_options_layout.addWidget(self.cb_trailers, 0, 0)
        extra_folder_options_layout.addWidget(self.cb_behind_the_scenes, 0, 1)
        extra_folder_options_layout.addWidget(self.cb_deleted_scenes, 0, 2)
        extra_folder_options_layout.addWidget(self.cb_featurettes, 0, 3)
        extra_folder_options_layout.addWidget(self.cb_interviews, 1, 0)
        extra_folder_options_layout.addWidget(self.cb_scenes, 1, 1)
        extra_folder_options_layout.addWidget(self.cb_shorts, 1, 2)
        extra_folder_options_layout.addWidget(self.cb_other, 1, 3)
        self.groupbox_extra_folder_options = qtw.QGroupBox("Extra Folder Options", self)
        self.groupbox_extra_folder_options.setLayout(extra_folder_options_layout)
        self.groupbox_extra_folder_options.setStyleSheet("""
            QGroupBox {
                border: 2px solid grey;
                border-radius: 5px;
                padding-top: 16px;
                font-weight: bold;
            }
        """)

        ## buttons at bottom
        self.btn_create = qtw.QPushButton("Create", self)
        self.btn_create.setEnabled(False)
        self.btn_create.clicked.connect(self.start_folder_generation)
        self.btn_cancel = qtw.QPushButton("Cancel", self)
        self.btn_cancel.clicked.connect(self.reject)
        create_or_cancel_buttons_layout = qtw.QHBoxLayout()
        create_or_cancel_buttons_layout.addWidget(self.btn_create)
        create_or_cancel_buttons_layout.addWidget(self.btn_cancel)

        # Set up the layout of window
        main_layout = qtw.QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.addLayout(select_directory_layout)
        main_layout.addWidget(self.groupbox_media_information)
        main_layout.addWidget(self.groupbox_tv_show_options)
        main_layout.addWidget(self.groupbox_extra_folder_options)
        main_layout.addLayout(create_or_cancel_buttons_layout)
        self.setLayout(main_layout)

    @qtc.Slot()
    def enable_or_disable_create_btn(self) -> None:
        enable_button = False
        if self.le_selected_directory.text() != "":
            if not self.le_media_title.text().isspace() and (len(self.le_media_title.text()) > 0):
                enable_button = True
        self.btn_create.setEnabled(enable_button)

    @qtc.Slot()
    def enable_or_disable_tv_show_options(self) -> None:
        if self.rb_media_type_movie_select.isChecked():
            self.groupbox_tv_show_options.setEnabled(False)
        elif self.rb_media_type_tv_select.isChecked():
            self.groupbox_tv_show_options.setEnabled(True)
        else:
            pass

    @qtc.Slot()
    def select_directory_popup(self) -> None:
        directory = qtw.QFileDialog.getExistingDirectory(
            self, "Select folder...", qtc.QDir.homePath()
        )

        if directory:
            self.le_selected_directory.setText(directory)
            self.enable_or_disable_create_btn()

    @qtc.Slot()
    def start_folder_generation(self) -> None:
        """
        Create the object that holds the information about the new media folder and disable all button widgets before
        sending it off.
        """
        # Create object that will the information about the media folder to create
        new_media_folder_info = GenerateMediaFolder()
        new_media_folder_info.directory = self.le_selected_directory.text()
        new_media_folder_info.media_title = self.le_media_title.text()
        new_media_folder_info.edition_tag = self.le_edition_tag.text()
        new_media_folder_info.media_type = (
            MediaCategory.MOVIE
            if self.rb_media_type_movie_select.isChecked()
            else MediaCategory.TV
        )
        new_media_folder_info.number_of_seasons = int(self.sb_number_of_seasons.text())
        new_media_folder_info.specials_season = (
            True if self.cb_specials_season_folder.isChecked() else False
        )
        new_media_folder_info.extra_folders["trailers"] = self.cb_trailers.isChecked()
        new_media_folder_info.extra_folders["behind the scenes"] = (
            self.cb_behind_the_scenes.isChecked()
        )
        new_media_folder_info.extra_folders["deleted scenes"] = (
            self.cb_deleted_scenes.isChecked()
        )
        new_media_folder_info.extra_folders["featurettes"] = (
            self.cb_featurettes.isChecked()
        )
        new_media_folder_info.extra_folders["interviews"] = (
            self.cb_interviews.isChecked()
        )
        new_media_folder_info.extra_folders["scenes"] = self.cb_scenes.isChecked()
        new_media_folder_info.extra_folders["shorts"] = self.cb_shorts.isChecked()
        new_media_folder_info.extra_folders["other"] = self.cb_other.isChecked()

        self._enable_or_disable_buttons(False)

        self.signal_initiate_create_media_folder.emit(new_media_folder_info)

    @qtc.Slot()
    def messagebox_media_folder_already_exists(self) -> None:
        """
        Launches the messagebox to inform user the media folder they wish to make already exists.
        Will reset the progress bar once user closes the messagebox window and enable all buttons.

        :return:
        """
        response = qtw.QMessageBox.information(
            self,
            "Media Folder Already Exists",
            'The Media Folder you wish to make already exists. Please click "ok" to cancel creation of Media Folder.',
        )

        if response == qtw.QMessageBox.StandardButton.Ok:
            self.signal_reset_progress_bar.emit()
            self._enable_or_disable_buttons(True)

    @qtc.Slot()
    def messagebox_media_folder_creation_complete(self) -> None:
        """
        Launches the messagebox to inform user the creation of the media folder is complete.
        Will reset the progress bar and enable all buttons to allow user to enter a new media folder.

        :return:
        """
        response = qtw.QMessageBox.information(
            self,
            "Create Media Folder Complete!",
            "Finished creating the media folder in the directory.",
        )

        if response == qtw.QMessageBox.StandardButton.Ok:
            self.signal_reset_progress_bar.emit()
            self._enable_or_disable_buttons(True)

    @qtc.Slot()
    def enable_buttons_due_to_error(self) -> None:
        """
        Enables all button widgets due to error.

        :return:
        """
        self._enable_or_disable_buttons(True)

    def _enable_or_disable_buttons(self, enable_or_disable: bool) -> None:
        """
        Enables / disables widgets and groupboxes.

        :param enable_or_disable: Sets the enable / disable status
        :return:
        """
        self.btn_create.setEnabled(enable_or_disable)
        self.btn_cancel.setEnabled(enable_or_disable)
        self.btn_select_directory.setEnabled(enable_or_disable)
        self.le_selected_directory.setEnabled(enable_or_disable)
        self.groupbox_media_information.setEnabled(enable_or_disable)
        if self.rb_media_type_tv_select.isChecked(): # only enable tv show options if user previously selected tv show for media type
            self.groupbox_tv_show_options.setEnabled(enable_or_disable)
        self.groupbox_extra_folder_options.setEnabled(enable_or_disable)
