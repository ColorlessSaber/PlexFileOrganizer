"""
Thread for Auto Update Media Files
"""
from PySide6 import QtCore as qtc
from ..classes import FolderAndFilePatterns
from ..functions import (
    update_files_in_directory,
    generate_correct_video_file_format,
    find_media_files_in_dir,
    video_file_condition,
    skip_extra_folders,
    default_folder_condition
)

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

            # set up the generator that will return the media files in a given directory based on options selected by
            # user
            if self.directory_and_options['scan_extra_folder']:
                generator_find_media_files = find_media_files_in_dir(video_file_condition, default_folder_condition, self.directory_and_options['directory'])
            else:
                generator_find_media_files = find_media_files_in_dir(video_file_condition, skip_extra_folders, self.directory_and_options['directory'])

            for file_list in generator_find_media_files:
                # check to see if all files in folder are formatted correctly
                all_files_are_formatted_correctly = folder_and_file_pattern.check_files_in_list(file_list)
                if not all_files_are_formatted_correctly:
                    print("generate correct file formats") # debug
                    #files_to_be_updated, message_number_of_files_affected = generate_correct_video_file_format(file_list)
                    #update_files_in_directory(files_to_be_updated)
                    #self.signals.progress.emit(50, message_number_of_files_affected)
            # print('finished the check') # for debugging
            self.signals.progress.emit(100, 'Finished scanning.')
            self.signals.finished.emit('auto_update')

        except OSError as e:
            self.signals.error.emit(e)

        except BaseException as e:
            # bad use of an exception, but required to catch an error for something that isn't covered for.
            self.signals.error.emit(e)