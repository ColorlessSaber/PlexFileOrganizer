"""
Thread for Auto Update Media Files
"""
import pathlib
from PySide6 import QtCore as qtc
from PlexFileOrganizer.functions import (update_files_in_directory,
                                         FolderAndFilePatterns,
                                         generate_correct_video_file_format,
                                         find_media_files_in_dir,
                                         video_file_condition)

class ThreadSignals(qtc.QObject):
    """
    The signals for the thread
    """
    error = qtc.Signal(object)
    finished = qtc.Signal(str)
    progress = qtc.Signal(int, str)

class AutoUpdateMediaFilesThread(qtc.QRunnable):

    def __init__(self, directory_and_options):
        """

        :param directory_and_options: The directory that contains the directory user selected, and other selectable options.
        """
        super().__init__()
        self.directory_and_options = directory_and_options
        self.signals = ThreadSignals()

    @qtc.Slot()
    def run(self):
        """
        Initialize the thread

        :return:
        """
        folder_and_file_pattern = FolderAndFilePatterns()

        try:
            self.signals.progress.emit(50, 'Scanning directory...')
            for file_list in find_media_files_in_dir(video_file_condition, self.directory_and_options['directory']):
                # Skip checking the video files in an Extra Folder, unless the option in directory_and_options
                # says we need to check them.
                # When the 'scan_extra_folder' folder is set to false, the media file in the Extra folder is skipped -- I.E.,
                # its assumed the file is formated correctly.
                if folder_and_file_pattern.extra_folder_check(file_list[0]) and not self.directory_and_options['scan_extra_folder']:
                    continue

                # check to see if all files in folder are formatted correctly
                all_files_are_formatted_correctly = folder_and_file_pattern.check_files_in_folder(file_list)
                if not all_files_are_formatted_correctly:
                    files_to_be_updated, message_number_of_files_affected = generate_correct_video_file_format(file_list)
                    update_files_in_directory(files_to_be_updated)
                    self.signals.progress.emit(50, message_number_of_files_affected)
                else:
                    continue

            # print('finished the check') # for debugging
            self.signals.progress.emit(100, 'Finished scanning.')
            self.signals.finished.emit('auto_update')

        except OSError as e:
            self.signals.error.emit(e)

        except BaseException as e:
            # bad use of an exception, but required to catch an error for something that isn't covered for.
            self.signals.error.emit(e)