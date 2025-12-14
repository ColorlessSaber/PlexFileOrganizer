"""
Thread for Manual Update Media Files
"""
import time
from PySide6 import QtCore as qtc
from ..classes import DefaultThreadSignals
from ..functions import update_files_in_directory

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
        try:
            self.signals.progress.emit(17, 'Starting manual update of media file(s)...')

            self.signals.progress.emit(24, '-- Prepping file(s) for update.')
            time.sleep(1)  # delay for a second so the user sees the program is working.
            # Create a list where each element is a tuple and each tuple contains the following
            # (old file name, new file name)
            prepped_media_files = []
            for media_file in self.media_files_to_update:
                prepped_media_files.append((media_file[0] + "/" + media_file[1] + media_file[3], media_file[0] + "/" + media_file[2] + media_file[3]))
            self.signals.progress.emit(41, '-- File(s) prepped for updating')

            time.sleep(1) # delay for a second so the user sees the program is working.
            self.signals.progress.emit(58, "-- Updating media file(s).")
            update_files_in_directory(prepped_media_files)
            self.signals.progress.emit(75, "-- Media file(s) updated.")

            time.sleep(1)  # delay for a second so the user sees the program is working.
            self.signals.progress.emit(100, 'Finished manual update of media file(s).')
            self.signals.finished.emit()

        except OSError as e:
            self.signals.error.emit(e)

        except BaseException as e:
            # bad use of an exception, but required to catch an error for something that isn't covered for.
            self.signals.error.emit(e)