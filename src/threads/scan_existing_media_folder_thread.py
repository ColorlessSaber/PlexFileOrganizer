"""
Thread for creating the media folders in the selected directory
"""

import time
import logging
from PySide6 import QtCore as qtc
from ..functions import scan_media_folder
from ..classes import DefaultThreadSignals


class ScanExistingMediaFolderThread(qtc.QRunnable):
    class ThreadSignals(DefaultThreadSignals):
        """
        The signals for the thread
        """

        finished = qtc.Signal(
            object
        )  # overwritten to emit an object when thread is finished
        not_media_folder = qtc.Signal()

    def __init__(self, media_folder_directory):
        super().__init__()
        self.media_folder_directory = media_folder_directory
        self.signals = self.ThreadSignals()

    @qtc.Slot()
    def run(self) -> None:
        """
        Initialize the thread
        """
        try:
            self.signals.progress.emit(25, "Scanning existing media folder...")
            time.sleep(1)  # delay for a second so the user sees the program is working.
            media_folder_information, folder_is_a_media_folder = scan_media_folder(
                self.media_folder_directory
            )

            self.signals.progress.emit(100, "Scan complete!")
            if folder_is_a_media_folder:
                self.signals.finished.emit(media_folder_information)
            else:
                self.signals.not_media_folder.emit()

        except OSError as e:
            logging.exception(e)
            self.signals.error.emit()

        except Exception as e:
            logging.exception(e)
            self.signals.error.emit()
