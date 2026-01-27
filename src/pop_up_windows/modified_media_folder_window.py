"""
Pop-up window to allow user to add more folders to an existing media folder
"""
from PySide6 import (
    QtWidgets as qtw,
    QtCore as qtc
)
from ..classes import ModifyMediaFolder, MediaCategory

class ModifiedMediaFolderWindow(qtw.QDialog):
    signal_initiate_scan_of_media_folder = qtc.Signal(str)
    signal_reset_progress_bar = qtc.Signal()
    signal_media_folder_update_information = qtc.Signal(object)

    def __init__(self, parent=None):
        """
        Dialog window to allow user to select an existing Media Folder and add more folders--extra or season folders--
        to it.

        :param parent: The parent window the dialog window will be linked to.
        """
        # The modal=True makes sure the user cannot click the main screen until they close the popup
        super().__init__(parent, modal=True)
        self.setWindowTitle('Modified Existing Media Folder')

        # widgets
        ## select a directory
        select_directory_layout = qtw.QGridLayout()
        self.btn_select_directory = qtw.QPushButton('Select Media Folder', self)
        self.btn_select_directory.setFocusPolicy(qtc.Qt.FocusPolicy.NoFocus)
        self.le_selected_directory = qtw.QLineEdit(self)
        self.le_selected_directory.returnPressed.connect(self.user_pasted_in_directory)
        self.btn_select_directory.clicked.connect(self.select_media_folder)
        select_directory_layout.addWidget(self.btn_select_directory, 0, 0)
        select_directory_layout.addWidget(self.le_selected_directory, 0, 1, 0, 2)

        ## display information about Media Folder
        self.media_title = qtw.QLabel('', self)
        self.media_type = qtw.QLabel('', self)
        self.highest_season_number = qtw.QLabel('', self)
        self.specials_season_folder_status = qtw.QLabel('', self)
        label_media_title = qtw.QLabel('Title:', self)
        label_media_title.setObjectName('media_title')
        label_media_category = qtw.QLabel('Category:', self)
        label_media_category.setObjectName('media_category')
        label_media_highest_season_number = qtw.QLabel('Highest Season Number Found:', self)
        label_media_highest_season_number.setObjectName('media_highest_season_number')
        label_media_specials_season_folder = qtw.QLabel('Specials Season Folder Status:', self)
        label_media_specials_season_folder.setObjectName('media_specials_season_folder')
        media_inform_form = qtw.QFormLayout()
        media_inform_form.addRow(label_media_title, self.media_title)
        media_inform_form.addRow(label_media_category, self.media_type)
        media_inform_form.addRow(label_media_highest_season_number, self.highest_season_number)
        media_inform_form.addRow(label_media_specials_season_folder, self.specials_season_folder_status)
        media_inform_form.setFormAlignment(qtc.Qt.AlignmentFlag.AlignLeft)
        media_inform_form.setSpacing(10)
        groupbox_media_information = qtw.QGroupBox('Media Information', self)
        groupbox_media_information.setLayout(media_inform_form)
        groupbox_media_information.setStyleSheet("""
            QGroupBox {
                border: 2px solid grey;
                border-radius: 5px;
                padding-top: 16px;
                font-weight: bold;
            }
            
            #media_title, #media_category, #media_highest_season_number, #media_specials_season_folder {
                text-decoration: underline;
            }
        """)

        ## TV show options
        self.sb_number_of_new_seasons = qtw.QSpinBox(self, value=0, minimum=0, maximum=100, singleStep=1)
        self.cb_generate_specials_season_folder = qtw.QCheckBox('Yes', self)
        label_number_of_new_seasons = qtw.QLabel('How many more Season to add?', self)
        label_generate_specials_folder = qtw.QLabel('Generate Specials Season Folder?', self)
        tv_show_options_form = qtw.QFormLayout()
        tv_show_options_form.addRow(label_number_of_new_seasons, self.sb_number_of_new_seasons)
        tv_show_options_form.addRow(label_generate_specials_folder, self.cb_generate_specials_season_folder)
        tv_show_options_form.setFormAlignment(qtc.Qt.AlignmentFlag.AlignLeft)
        self.groupbox_tv_show_options = qtw.QGroupBox('TV Show Options', self)
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

        ## extra folder options
        self.cb_trailers = qtw.QCheckBox('Trailers', self)
        self.cb_behind_the_scenes = qtw.QCheckBox('Behind The Scenes', self)
        self.cb_deleted_scenes = qtw.QCheckBox('Deleted Scenes', self)
        self.cb_featurettes = qtw.QCheckBox('Featurettes', self)
        self.cb_interviews = qtw.QCheckBox('Interviews', self)
        self.cb_scenes = qtw.QCheckBox('Scenes', self)
        self.cb_shorts = qtw.QCheckBox('shorts', self)
        self.cb_other = qtw.QCheckBox('Other', self)
        extra_folder_options_layout = qtw.QGridLayout()
        extra_folder_options_layout.addWidget(self.cb_trailers, 0, 0)
        extra_folder_options_layout.addWidget(self.cb_behind_the_scenes, 0, 1)
        extra_folder_options_layout.addWidget(self.cb_deleted_scenes, 0, 2)
        extra_folder_options_layout.addWidget(self.cb_featurettes, 0, 3)
        extra_folder_options_layout.addWidget(self.cb_interviews, 1, 0)
        extra_folder_options_layout.addWidget(self.cb_scenes, 1, 1)
        extra_folder_options_layout.addWidget(self.cb_shorts, 1, 2)
        extra_folder_options_layout.addWidget(self.cb_other, 1, 3)
        self.groupbox_extra_folder_options = qtw.QGroupBox('Extra Folder Options', self)
        self.groupbox_extra_folder_options.setLayout(extra_folder_options_layout)
        self.groupbox_extra_folder_options.setStyleSheet("""
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

        ## buttons at bottom
        self.btn_update = qtw.QPushButton('Update', self)
        self.btn_update.setEnabled(False)
        self.btn_update.clicked.connect(self.start_folder_modification)
        self.btn_cancel = qtw.QPushButton('Cancel', self)
        self.btn_cancel.clicked.connect(self.reject)
        create_or_cancel_buttons_layout = qtw.QHBoxLayout()
        create_or_cancel_buttons_layout.addWidget(self.btn_update)
        create_or_cancel_buttons_layout.addWidget(self.btn_cancel)

        # Set up the layout of window
        main_layout = qtw.QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.addLayout(select_directory_layout)
        main_layout.addWidget(groupbox_media_information)
        main_layout.addWidget(self.groupbox_tv_show_options)
        main_layout.addWidget(self.groupbox_extra_folder_options)
        main_layout.addLayout(create_or_cancel_buttons_layout)
        self.setLayout(main_layout)

    @qtc.Slot(object)
    def load_existing_media_folder_info(self, media_file_information) -> None:
        """
        Load in the existing media folder information and update the dialog window with this
        information.

        :param media_file_information: The media folder information.
        """
        self.signal_reset_progress_bar.emit()
        self.le_selected_directory.setText(media_file_information.directory)
        self.media_title.setText(media_file_information.media_title)
        self.media_type.setText(media_file_information.media_type)

        if media_file_information.media_type.is_tv():
            self.highest_season_number.setText(f'{media_file_information.number_of_seasons}')
            if media_file_information.specials_season:
                self.specials_season_folder_status.setText('Exists')
                self.cb_generate_specials_season_folder.setChecked(True)
                self.cb_generate_specials_season_folder.setEnabled(False)
            else:
                self.specials_season_folder_status.setText('Does not exist')
                self.cb_generate_specials_season_folder.setChecked(False)
                self.cb_generate_specials_season_folder.setEnabled(True)
            self.sb_number_of_new_seasons.setValue(0)
            self.sb_number_of_new_seasons.setEnabled(True)
        elif media_file_information.media_type.is_movie():
            self.highest_season_number.setText('N/A')
            self.specials_season_folder_status.setText('N/A')
            self.cb_generate_specials_season_folder.setChecked(False)
            self.cb_generate_specials_season_folder.setEnabled(False)
            self.sb_number_of_new_seasons.setValue(0)
            self.sb_number_of_new_seasons.setEnabled(False)

        if media_file_information.extra_folders['trailers']:
            self.cb_trailers.setChecked(True)
            self.cb_trailers.setEnabled(False)
        else:
            self.cb_trailers.setChecked(False)
            self.cb_trailers.setEnabled(True)

        if media_file_information.extra_folders['behind the scenes']:
            self.cb_behind_the_scenes.setChecked(True)
            self.cb_behind_the_scenes.setEnabled(False)
        else:
            self.cb_behind_the_scenes.setChecked(False)
            self.cb_behind_the_scenes.setEnabled(True)

        if media_file_information.extra_folders['deleted scenes']:
            self.cb_deleted_scenes.setChecked(True)
            self.cb_deleted_scenes.setEnabled(False)
        else:
            self.cb_deleted_scenes.setChecked(False)
            self.cb_deleted_scenes.setEnabled(True)

        if media_file_information.extra_folders['featurettes']:
            self.cb_featurettes.setChecked(True)
            self.cb_featurettes.setEnabled(False)
        else:
            self.cb_featurettes.setChecked(False)
            self.cb_featurettes.setEnabled(True)

        if media_file_information.extra_folders['interviews']:
            self.cb_interviews.setChecked(True)
            self.cb_interviews.setEnabled(False)
        else:
            self.cb_interviews.setChecked(False)
            self.cb_interviews.setEnabled(True)

        if media_file_information.extra_folders['scenes']:
            self.cb_scenes.setChecked(True)
            self.cb_scenes.setEnabled(False)
        else:
            self.cb_scenes.setChecked(False)
            self.cb_scenes.setEnabled(True)

        if media_file_information.extra_folders['shorts']:
            self.cb_shorts.setChecked(True)
            self.cb_shorts.setEnabled(False)
        else:
            self.cb_shorts.setChecked(False)
            self.cb_shorts.setEnabled(True)

        if media_file_information.extra_folders['other']:
            self.cb_other.setChecked(True)
            self.cb_other.setEnabled(False)
        else:
            self.cb_other.setChecked(False)
            self.cb_other.setEnabled(True)

        self.btn_update.setEnabled(True)

    def select_media_folder(self) -> None:
        media_folder_dir = qtw.QFileDialog.getExistingDirectory(
            self,
            'Select Media Folder...',
            qtc.QDir.homePath()
        )

        if media_folder_dir: # confirm the user selected a directory
            self.signal_initiate_scan_of_media_folder.emit(media_folder_dir)

    def user_pasted_in_directory(self) -> None:
        self.signal_initiate_scan_of_media_folder.emit(self.le_selected_directory.text())

    @qtc.Slot()
    def start_folder_modification(self) -> None:
        """
        Create the object to hold the user's selection and disable all button widgets before sending it off.
        """
        modified_media_folder_info = ModifyMediaFolder()
        modified_media_folder_info.directory = self.le_selected_directory.text()
        modified_media_folder_info.media_title = self.media_title.text()
        modified_media_folder_info.media_type = MediaCategory.MOVIE if self.media_type.text().lower() == 'movie' else MediaCategory.TV
        modified_media_folder_info.number_of_seasons = int(self.highest_season_number.text()) if self.highest_season_number.text() != '' else 0
        modified_media_folder_info.number_of_new_seasons = int(self.sb_number_of_new_seasons.text())
        modified_media_folder_info.specials_season = self.cb_generate_specials_season_folder.isChecked() if self.cb_generate_specials_season_folder.isEnabled() else False
        modified_media_folder_info.extra_folders['trailers'] = self.cb_trailers.isChecked() if self.cb_trailers.isEnabled() else False
        modified_media_folder_info.extra_folders['behind the scenes'] = self.cb_behind_the_scenes.isChecked() if self.cb_behind_the_scenes.isEnabled() else False
        modified_media_folder_info.extra_folders['deleted scenes'] = self.cb_deleted_scenes.isChecked() if self.cb_deleted_scenes.isEnabled() else False
        modified_media_folder_info.extra_folders['featurettes'] = self.cb_featurettes.isChecked() if self.cb_featurettes.isEnabled() else False
        modified_media_folder_info.extra_folders['interviews'] = self.cb_interviews.isChecked() if self.cb_interviews.isEnabled() else False
        modified_media_folder_info.extra_folders['scenes'] = self.cb_scenes.isChecked() if self.cb_scenes.isEnabled() else False
        modified_media_folder_info.extra_folders['shorts'] = self.cb_shorts.isChecked() if self.cb_shorts.isEnabled() else False
        modified_media_folder_info.extra_folders['other'] = self.cb_other.isChecked() if self.cb_other.isEnabled() else False

        self._enable_or_disable_buttons(False)

        self.signal_media_folder_update_information.emit(modified_media_folder_info)

    @qtc.Slot()
    def messagebox_folder_not_media_folder(self) -> None:
        """
        Launches the messagebox to inform user the folder is not media folder.
        Will reset the progress bar and enable the button widgets.

        :return:
        """
        response = qtw.QMessageBox.information(
            self,
            'Selected Folder is not Media Folder!',
            'The folder you selected to analyze is not a Media Folder.'
        )

        if response == qtw.QMessageBox.StandardButton.Ok:
            self.signal_reset_progress_bar.emit()
            self._enable_or_disable_buttons(True)

    @qtc.Slot()
    def messagebox_media_folder_modification_complete(self) -> None:
        """
        Launches a messagebox to inform user the update of the media folder is complete.
        Will reset the progress bar, reset the information in the window, and enable the button widgets.

        :return:
        """
        response = qtw.QMessageBox.information(
            self,
            'Update Media Folder Complete!',
            'Finished updating the media folder in the directory.'
        )

        if response == qtw.QMessageBox.StandardButton.Ok:
            self.signal_reset_progress_bar.emit()
            self._clear_scanned_media_folder_information()
            self._enable_or_disable_buttons(True)

    @qtc.Slot()
    def enable_buttons_due_to_error(self) -> None:
        """
        Enables all button widgets due to error.

        :return:
        """
        self._enable_or_disable_buttons(True)

    def _clear_scanned_media_folder_information(self) -> None:
        """
        Clears the information that was scanned from the media folder.

        :return:
        """
        self.le_selected_directory.setText("")
        self.media_title.setText("")
        self.media_type.setText("")
        self.highest_season_number.setText("")
        self.specials_season_folder_status.setText("")
        self.sb_number_of_new_seasons.setValue(0)
        self.cb_generate_specials_season_folder.setChecked(False)
        self.cb_trailers.setChecked(False)
        self.cb_trailers.setEnabled(True)
        self.cb_behind_the_scenes.setChecked(False)
        self.cb_behind_the_scenes.setEnabled(True)
        self.cb_deleted_scenes.setChecked(False)
        self.cb_deleted_scenes.setEnabled(True)
        self.cb_featurettes.setChecked(False)
        self.cb_featurettes.setEnabled(True)
        self.cb_shorts.setChecked(False)
        self.cb_shorts.setEnabled(True)
        self.cb_interviews.setChecked(False)
        self.cb_interviews.setEnabled(True)
        self.cb_scenes.setChecked(False)
        self.cb_scenes.setEnabled(True)
        self.cb_other.setChecked(False)
        self.cb_other.setEnabled(True)

    def _enable_or_disable_buttons(self, enable_or_disable: bool) -> None:
        """
        Enables / disables the button widgets.

        :param enable_or_disable: Sets the enable / disable status
        :return:
        """
        self.btn_select_directory.setEnabled(enable_or_disable)
        self.btn_cancel.setEnabled(enable_or_disable)
        self.btn_update.setEnabled(enable_or_disable)
        self.le_selected_directory.setEnabled(enable_or_disable)
        self.groupbox_tv_show_options.setEnabled(enable_or_disable)
        self.groupbox_extra_folder_options.setEnabled(enable_or_disable)