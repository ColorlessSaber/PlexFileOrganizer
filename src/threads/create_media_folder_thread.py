"""
Thread for creating the media folders in the selected directory
"""

import time
import logging
from PySide6 import QtCore as qtc
from ..classes import DefaultThreadSignals


class CreateMediaFolderThread(qtc.QRunnable):
    class ThreadSignals(DefaultThreadSignals):
        """
        The signals for thread
        """

        media_folder_already_exists = qtc.Signal()

    def __init__(self, media_folder_information):
        super().__init__()
        self.media_folder_information = media_folder_information
        self.signals = self.ThreadSignals()

    @qtc.Slot()
    def run(self) -> None:
        """
        Initialize the thread
        :return:
        """

        try:
            self.signals.progress.emit(9, "Checking if Media Folder Exists...")
            time.sleep(1)  # delay for one second so user sees the program is working.
            if self.media_folder_information.check_if_media_folder_exists():
                self.signals.progress.emit(0, "Canceling creation of Media Folder.")
                self.signals.media_folder_already_exists.emit()
            else:
                self.signals.progress.emit(
                    18,
                    "Folder does not exist. Starting the process of creating Media Folder for: "
                    + self.media_folder_information.media_title,
                )

                self.signals.progress.emit(27, "-- Creating media folder.")
                time.sleep(
                    1
                )  # delay for one second so user sees the program is working.
                self.media_folder_information.generate_media_folder()
                self.signals.progress.emit(36, "-- Folder created.")

                if self.media_folder_information.media_type.is_tv():
                    self.signals.progress.emit(45, "-- Creating season folder(s).")
                    time.sleep(
                        1
                    )  # delay for one second so user sees the program is working.
                    self.media_folder_information.generate_seasons()
                    self.signals.progress.emit(54, "-- Season folder(s) created.")

                    if self.media_folder_information.specials_season:
                        self.signals.progress.emit(
                            63, "-- Generating Specials season folder."
                        )
                        time.sleep(
                            1
                        )  # delay for a second so the user sees the program is working.
                        self.media_folder_information.generate_specials_season_folder()
                        self.signals.progress.emit(
                            72, "-- Specials season folder generated."
                        )
                    else:
                        self.signals.progress.emit(
                            72, "-- Skipping Specials season folder generation."
                        )
                else:
                    self.signals.progress.emit(
                        72,
                        "-- Media folder is for movie; no seasons and/or Specials season folder will be generated.",
                    )

                if self.media_folder_information.check_if_new_extra_folders_are_needed():
                    self.signals.progress.emit(81, "-- Creating extra folder(s).")
                    time.sleep(
                        1
                    )  # delay for one second so user sees the program is working.
                    self.media_folder_information.generate_extra_folders()
                    self.signals.progress.emit(90, "-- Extra folder(s) created.")
                else:
                    self.signals.progress.emit(
                        90, "-- No extra folder(s) needed to be created."
                    )

                self.signals.progress.emit(100, "Finished generating Media Folder!")
                self.signals.finished.emit()

        except (OSError, FileExistsError) as e:
            logging.exception(e)
            self.signals.error.emit(e)

        except Exception as e:
            logging.exception(e)
            self.signals.error.emit(e)
