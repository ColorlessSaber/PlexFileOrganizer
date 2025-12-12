"""
Pop-up window to allow user to add more folders to an existing media folder
"""
from PySide6 import (
    QtWidgets as qtw,
    QtCore as qtc)
from ..classes import ModifyMediaFolder

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
        select_directory_layout = qtw.QGridLayout()
        self.btn_select_directory = qtw.QPushButton('Select Media Folder', self)
        self.select_directory_label = qtw.QLabel('', self)
        self.btn_select_directory.clicked.connect(self.select_media_folder)
        select_directory_layout.addWidget(self.btn_select_directory, 0, 0)
        select_directory_layout.addWidget(self.select_directory_label, 0, 1, 0, 2)

        media_inform_form = qtw.QFormLayout()
        self.media_title = qtw.QLabel('', self)
        self.media_type = qtw.QLabel('', self)
        media_inform_form.addRow('Media Title:', self.media_title)
        media_inform_form.addRow('Media Type:', self.media_type)
        media_inform_form.setFormAlignment(qtc.Qt.AlignmentFlag.AlignLeft)

        self.season_inform_form = qtw.QFormLayout()
        self.highest_season_number = qtw.QLabel('', self)
        self.number_of_new_seasons = qtw.QSpinBox(
            self,
            value=0,
            minimum=0,
            maximum=100,
            singleStep=1
        )
        self.season_inform_form.addRow('Highest Season Number found:', self.highest_season_number)
        self.season_inform_form.addRow('How many more Season to add?', self.number_of_new_seasons)
        self.season_inform_form.setFormAlignment(qtc.Qt.AlignmentFlag.AlignLeft)

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

        self.btn_update = qtw.QPushButton('Update', self)
        self.btn_update.setEnabled(False)
        self.btn_update.clicked.connect(self.start_folder_modification)

        self.btn_cancel = qtw.QPushButton('Cancel', self)
        self.btn_cancel.clicked.connect(self.reject)

        # Set up the layout of window
        main_layout = qtw.QVBoxLayout()
        main_layout.addLayout(select_directory_layout)
        main_layout.addLayout(media_inform_form)
        main_layout.addLayout(self.season_inform_form)
        main_layout.addLayout(extra_folder_layout)
        main_layout.addWidget(self.btn_update)
        main_layout.addWidget(self.btn_cancel)
        self.setLayout(main_layout)

    @qtc.Slot(object)
    def load_existing_media_folder_info(self, media_file_information) -> None:
        """
        Load in the existing media folder information and update the dialog window with this
        information.

        :param media_file_information: The media folder information.
        """
        self.signal_reset_progress_bar.emit()
        self.select_directory_label.setText(media_file_information.directory)
        self.media_title.setText(media_file_information.media_title)
        self.media_type.setText(media_file_information.media_type)

        if media_file_information.media_type == 'tv':
            self.season_inform_form.setRowVisible(0, True)
            self.highest_season_number.setText(f'{media_file_information.number_of_seasons}')
            self.season_inform_form.setRowVisible(1, True)
            self.number_of_new_seasons.setValue(0)
        else:
            self.season_inform_form.setRowVisible(0, False)
            self.highest_season_number.setText('')
            self.season_inform_form.setRowVisible(1, False)
            self.number_of_new_seasons.setValue(0)

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

    @qtc.Slot()
    def start_folder_modification(self) -> None:
        """
        Create the object to hold the user's selection and disable all button widgets before sending it off.
        """
        modified_media_folder_info = ModifyMediaFolder()
        modified_media_folder_info.directory = self.select_directory_label.text()
        modified_media_folder_info.media_title = self.media_title.text()
        modified_media_folder_info.media_type = self.media_type.text()
        modified_media_folder_info.number_of_seasons = int(self.highest_season_number.text())
        modified_media_folder_info.number_of_new_seasons = int(self.number_of_new_seasons.text())
        modified_media_folder_info.extra_folders['trailers'] = self.cb_trailers.isChecked() if self.cb_trailers.isEnabled() else False
        modified_media_folder_info.extra_folders['behind the scenes'] = self.cb_behind_the_scenes.isChecked() if self.cb_behind_the_scenes.isEnabled() else False
        modified_media_folder_info.extra_folders['deleted scenes'] = self.cb_deleted_scenes.isChecked() if self.cb_deleted_scenes.isEnabled() else False
        modified_media_folder_info.extra_folders['featurettes'] = self.cb_featurettes.isChecked() if self.cb_featurettes.isEnabled() else False
        modified_media_folder_info.extra_folders['interviews '] = self.cb_interviews.isChecked() if self.cb_interviews.isEnabled() else False
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

        if response == qtw.QMessageBox.Ok:
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

        if response == qtw.QMessageBox.Ok:
            self.signal_reset_progress_bar.emit()
            self._clear_scanned_media_folder_information()
            self._enable_or_disable_buttons(True)

    def _clear_scanned_media_folder_information(self) -> None:
        """
        Clears the information that was scanned from the media folder.

        :return:
        """
        self.select_directory_label.setText("")
        self.media_title.setText("")
        self.media_type.setText("")
        self.highest_season_number.setText("")
        self.number_of_new_seasons.setValue(0)
        self.cb_trailers.setChecked(False)
        self.cb_behind_the_scenes.setChecked(False)
        self.cb_deleted_scenes.setChecked(False)
        self.cb_featurettes.setChecked(False)
        self.cb_shorts.setChecked(False)
        self.cb_interviews.setChecked(False)
        self.cb_scenes.setChecked(False)
        self.cb_other.setChecked(False)


    def _enable_or_disable_buttons(self, enable_or_disable: bool) -> None:
        """
        Enables / disables the button widgets.

        :param enable_or_disable: Sets the enable / disable status
        :return:
        """
        self.btn_select_directory.setEnabled(enable_or_disable)
        self.btn_cancel.setEnabled(enable_or_disable)
        self.btn_update.setEnabled(enable_or_disable)
        self.cb_trailers.setEnabled(enable_or_disable)
        self.cb_behind_the_scenes.setEnabled(enable_or_disable)
        self.cb_deleted_scenes.setEnabled(enable_or_disable)
        self.cb_featurettes.setEnabled(enable_or_disable)
        self.cb_shorts.setEnabled(enable_or_disable)
        self.cb_interviews.setEnabled(enable_or_disable)
        self.cb_scenes.setEnabled(enable_or_disable)
        self.cb_other.setEnabled(enable_or_disable)