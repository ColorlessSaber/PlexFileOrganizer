"""
Thread for Auto Update Media Files
"""
import time
from PySide6 import QtCore as qtc
from ..classes import FolderAndFilePatterns, DefaultThreadSignals
from ..functions import (
    update_files_in_directory,
    generate_correct_video_file_format,
    find_media_files_in_dir,
    video_file_condition,
    skip_extra_folders,
    default_folder_condition
)

class AutoUpdateMediaFilesThread(qtc.QRunnable):
    class ThreadSignals(DefaultThreadSignals):
        """
        The signals for the thread
        """

    def __init__(self, directory_and_options):
        """

        :param directory_and_options: The directory that contains the directory user selected, and other selectable options.
        """
        super().__init__()
        self.directory_and_options = directory_and_options
        self.signals = self.ThreadSignals()

    @qtc.Slot()
    def run(self) -> None:
        """
        Initialize the thread

        :return:
        """
        try:
            self.signals.progress.emit(10, 'Beginning process of automatic update of media file(s).')
            time.sleep(1) # delay for a second so the user sees the program is working.
            message_number_of_files_affected = ""
            folder_and_file_pattern = FolderAndFilePatterns()

            # set up the generator that will return the media files in a given directory based on option(s) selected by
            # user
            if self.directory_and_options['scan_extra_folder']:
                self.signals.progress.emit(25, 'Prepping process to include extra folders in scan...')
                generator_find_media_files = find_media_files_in_dir(video_file_condition, default_folder_condition, self.directory_and_options['directory'])
            else:
                self.signals.progress.emit(25, 'Skipping prepping process to include extra folders in scan...')
                generator_find_media_files = find_media_files_in_dir(video_file_condition, skip_extra_folders, self.directory_and_options['directory'])

            time.sleep(1)  # delay for a second so the user sees the program is working.

            self.signals.progress.emit(30, 'Scanning directory and sub-folders...')

            for file_list in generator_find_media_files:
                all_files_are_formatted_correctly = folder_and_file_pattern.check_files_in_list(file_list)
                if not all_files_are_formatted_correctly:
                    #print("generate correct file formats") # debug
                    files_to_be_updated, message_number_of_files_affected = generate_correct_video_file_format(file_list)
                    update_files_in_directory(files_to_be_updated)
                    self.signals.progress.emit(50, message_number_of_files_affected)
                    time.sleep(1)  # delay for a second so the user sees the program is working.

            if not message_number_of_files_affected: # For when no files were found that needed updating
                self.signals.progress.emit(50, '-- No files were found that needed to be updated')

            self.signals.progress.emit(100, 'Finished scanning.')
            self.signals.finished.emit()

        except OSError as e:
            self.signals.error.emit(e)

        except BaseException as e:
            # bad use of an exception, but required to catch an error for something that isn't covered for.
            self.signals.error.emit(e)