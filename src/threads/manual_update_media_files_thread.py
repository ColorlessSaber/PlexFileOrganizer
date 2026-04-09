"""
Thread for Manual Update Media Files
"""

import time
import logging
from PySide6 import QtCore as qtc
from ..classes import DefaultThreadSignals
from ..functions import update_files_in_directory, prep_files_for_modified_renaming


class ManualUpdateMediaFilesThread(qtc.QRunnable):
    class ThreadSignals(DefaultThreadSignals):
        """
        The signals for the thread
        """

    def __init__(self, media_files_to_update: list) -> None:
        """
        Constructs the thread.

        :param media_files_to_update: List of media files to update.
        """
        super().__init__()
        self.media_files_to_update = media_files_to_update
        self.signals = self.ThreadSignals()

    @qtc.Slot()
    def run(self) -> None:
        """
        Starts the thread.
        """
        # To allow the ability to undo the identification of files in the directory if an error occurred.
        files_identified_for_renaming = None

        try:
            self.signals.progress.emit(17, "Starting manual update of media file(s)...")

            self.signals.progress.emit(24, "-- Prepping file(s) for update.")
            time.sleep(1)  # delay for a second so the user sees the program is working.
            files_identified_for_renaming, prepped_media_files = (
                prep_files_for_modified_renaming(self.media_files_to_update)
            )

            self.signals.progress.emit(
                41, "-- Identify the file(s) in directory to be renamed."
            )
            time.sleep(1)  # delay for a second so the user sees the program is working.
            update_files_in_directory(files_identified_for_renaming)

            self.signals.progress.emit(58, "-- Updating media file(s).")
            time.sleep(1)  # delay for a second so the user sees the program is working.
            update_files_in_directory(prepped_media_files)
            self.signals.progress.emit(75, "-- Media file(s) updated.")

            time.sleep(1)  # delay for a second so the user sees the program is working.
            self.signals.progress.emit(100, "Finished manual update of media file(s).")
            self.signals.finished.emit()

        except OSError as e:
            logging.exception(e)
            self.signals.error.emit(e)

        except Exception as e:
            logging.exception(e)
            self.signals.error.emit(e)
