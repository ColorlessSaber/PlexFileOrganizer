from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

from .model import Model
from .view import View


class MainWindow(qtw.QMainWindow):
    """The main window for the application"""

    def __init__(self):
        super().__init__()

        self.view = View()
        self.model = Model()
        self.setCentralWidget(self.view)
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        self.progress_bar = qtw.QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.statusBar().addPermanentWidget(self.progress_bar)

        self.statusBar().addPermanentWidget(qtw.QLabel('V1.1.1'))

        # view signals to be connected to model slots
        self.view.signal_initiate_creating_media_folder.connect(self.model.start_create_media_folder_thread)
        self.view.signal_user_confirmation_of_existing_media_folder.connect(self.model.signal_user_confirmation_of_existing_media_folder)
        self.view.signal_initiate_auto_update_media_files.connect(self.model.start_auto_update_media_files_thread)

        self.view.signal_initiate_scan_of_media_folder.connect(self.model.start_scan_of_existing_media_folder_thread)
        self.view.signal_initiate_update_of_media_folder.connect(self.model.start_update_of_existing_media_folder_thread)

        self.view.signal_check_list_of_files_for_duplicates.connect(self.model.check_for_duplicates_in_media_file_list)
        self.view.signal_initiate_manual_update.connect(self.model.start_manual_update_media_files_thread)

        # model signals to be connected to view slots
        self.model.signal_inform_user_media_folder_already_exists.connect(self.view.status_pass_through_media_folder_already_exists)
        self.model.signal_create_media_folder_finished.connect(self.view.status_pass_through_media_folder_creation_complete)

        self.model.signal_auto_update_finished.connect(self.view.messagebox_auto_update_media_files_complete)

        self.model.signal_inform_user_folder_not_media_folder.connect(self.view.status_pass_through_folder_not_media_folder)
        self.model.signal_analysis_of_media_folder_complete.connect(self.view.data_pass_through_media_folder_scan_result)
        self.model.signal_update_of_media_folder_finished.connect(self.view.status_pass_through_media_folder_modification_complete)

        self.model.signal_duplicate_files_check_complete.connect(self.view.data_pass_through_duplicate_check_result)
        self.model.signal_manual_update_finished.connect(self.view.status_pass_through_manual_update_media_files_complete)

        # view signals to be connected to main_window slots
        self.view.signal_reset_progress_bar.connect(self.slot_reset_progress_bar)
        self.view.signal_close_application.connect(self.close)

        # model signals to be connected to main_window slots
        self.model.signal_update_progress.connect(self.slot_update_progress_bar_and_print_message)
        self.model.signal_error_message.connect(self.slot_display_error_message)

        self.show()

    # *** Main Window Methods ***
    def closeEvent(self, event) -> None:
        """
        Close the application gracefully.
        """
        response = qtw.QMessageBox.question(
            self,
            'Close Application?',
            'Are you sure you want to close the application?',
            buttons= qtw.QMessageBox.Yes | qtw.QMessageBox.No,
            defaultButton= qtw.QMessageBox.Yes
        )

        if response == qtw.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # *** Slots for model/view inputs***
    @qtc.Slot(int, str)
    def slot_update_progress_bar_and_print_message(self, progress_bar_percentage: int, status_message: str) -> None:
        """
        Update the progress bar and print message on Log Window

        :param progress_bar_percentage: The int value for the progress bar
        :param status_message: Message to display on the status bar
        :return:
        """
        self.progress_bar.setValue(progress_bar_percentage)
        self.view.write_to_log_window(status_message)

    @qtc.Slot(object)
    def slot_display_error_message(self, error_message: object) -> None:
        """
        Write the error message to the Log Window, reset the progress bar, and have view launch messagebox
        to inform user what happened.

        :param error_message: The error that was generated
        :return:
        """
        self.progress_bar.reset()
        self.view.write_to_log_window('\n!!Error has been detected!! -> {}'.format(error_message))
        self.view.messagebox_system_error_detected()

    @qtc.Slot()
    def slot_reset_progress_bar(self) -> None:
        """
        Reset the progress bar

        :return:
        """
        self.progress_bar.reset()
