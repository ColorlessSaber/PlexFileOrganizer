"""
Thread for updating existing media folder
"""


import logging
from PySide6 import QtCore as qtc
from ..classes import DefaultThreadSignals
from ..functions import rename_media_folder_and_contents


class UpdateExistingMediaFolderThread(qtc.QRunnable):
    class ThreadSignals(DefaultThreadSignals):
        """
        The signals for thread
        """

    def __init__(self, info_of_media_folder):
        super().__init__()
        self.info_of_media_folder = info_of_media_folder
        self.signals = self.ThreadSignals()

    @qtc.Slot()
    def run(self) -> None:
        """
        Initialize the thread
        """
        try:
            self.signals.progress.emit(
                13,
                "Starting to update existing media folder: "
                + self.info_of_media_folder.media_title,
            )

            if self.info_of_media_folder.media_type.is_tv():
                if self.info_of_media_folder.number_of_new_seasons > 0:
                    self.signals.progress.emit(
                        26, "-- Generating more season folder(s)."
                    )
                    self.info_of_media_folder.generate_new_season_folders()
                    self.signals.progress.emit(39, "-- New season folder(s) generated.")
                else:
                    self.signals.progress.emit(
                        39, "-- No new season folder(s) needed to be created."
                    )

                if self.info_of_media_folder.specials_season:
                    self.signals.progress.emit(
                        52, "-- Generating Specials season folder."
                    )
                    self.info_of_media_folder.generate_specials_season_folder()
                    self.signals.progress.emit(
                        65, "-- Specials season folder generated."
                    )
                else:
                    self.signals.progress.emit(
                        65, "-- Skipping Specials season folder generation."
                    )
            else:
                self.signals.progress.emit(
                    65,
                    "-- Media folder is for movie; no seasons and/or Specials season folder will be generated.",
                )

            if self.info_of_media_folder.check_if_new_extra_folders_are_needed():
                self.signals.progress.emit(78, "-- Generating extra folder(s).")
                self.info_of_media_folder.generate_new_extra_folders()
                self.signals.progress.emit(91, "-- Extra folder(s) generated.")
            else:
                self.signals.progress.emit(
                    91, "-- No new extra folder(s) needed to be created."
                )

            # renaming of the folder and its contents is done last so it doesn't mess up adding new folders
            if not self.info_of_media_folder.new_media_title.isspace() and (self.info_of_media_folder.new_media_title != ""):
                self.signals.progress.emit(
                    15,
                    "-- Renaming media folder from {} to {}".format(
                        self.info_of_media_folder.media_title, self.info_of_media_folder.new_media_title
                    )
                )

                rename_media_folder_and_contents(
                    self.info_of_media_folder.media_title,
                    self.info_of_media_folder.new_media_title,
                    self.info_of_media_folder.directory,
                )
            else:
                self.signals.progress.emit(
                    15,
                    "-- Media folder name will be kept."
                )

            self.signals.progress.emit(100, "Update of Media Folder completed!")
            self.signals.finished.emit()

        except OSError as e:
            logging.exception(e)
            self.signals.error.emit()

        except Exception as e:
            logging.exception(e)
            self.signals.error.emit()
